# -*- coding: utf-8 -*-
"""AEO botas: uždavinėja promptų banko klausimus AI paieškoms ir matuoja, ar atsakymuose minimas Peter Bravvo.

Kas veikia:
- kiekvieną paleidimą ima kitą BATCH promptų porciją (eilė sukasi ratu, būsena aeo/busena.json);
- kiekvienam promptui klausia įjungtų tiekėjų (įjungta = yra raktas aplinkoje):
    PERPLEXITY_API_KEY  -> Perplexity Sonar (su paieška internete, grąžina šaltinius)   ~0,006 $/klausimas
    OPENROUTER_API_KEY  -> OPENROUTER_MODEL (numatytas meta-llama/llama-3.3-70b-instruct:free, 0 $, be paieškos;
                           galima keli per kablelį). Nemokamas limitas ~50 užklausų per dieną, todėl BATCH 45.
    GROQ_API_KEY        -> llama-3.3-70b (be paieškos: ką modelis „žino“), 0 $
- rezultatai: aeo/rezultatai/YYYY-MM-DD.csv ir aeo/rezultatai/SUVESTINE.md;
- MAX_USD riboja vieno paleidimo kainą (numatyta 1,00 $).

Svarbu: klausimų siuntimas AI NEMOKO AI apie Piotrą. Botas MATUOJA. Matomumą kelia svetainės turinys,
schema, citatos kituose šaltiniuose (žiniasklaida, katalogai, Google profilis, Wikidata).
"""
import csv, datetime, json, os, re, sys, time, urllib.request, urllib.error
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "rezultatai")
STATE = os.path.join(HERE, "busena.json")
BATCH = int(os.environ.get("BATCH", "45"))
MAX_USD = float(os.environ.get("MAX_USD", "1.0"))
MENTION = re.compile(r"peter\s*bravv?o|peterbravvo\.lt|andrzejewsk|and[žz]ejevsk|bravvo\s*band", re.I)
DOMAIN = "peterbravvo.lt"
SYS = {"lt": "Atsakyk lietuviškai, trumpai ir konkrečiai. Jei rekomenduoji žmones ar paslaugas Lietuvoje, nurodyk vardus.",
       "pl": "Odpowiedz po polsku, krótko i konkretnie. Jeśli polecasz osoby lub usługi na Litwie, podaj nazwiska.",
       "ru": "Ответь по-русски, кратко и конкретно. Если рекомендуешь людей или услуги в Литве, назови имена.",
       "en": "Answer in English, briefly and concretely. If you recommend people or services in Lithuania, name them."}


def post(url, key, body, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


PREF = ["llama-3.3-70b", "llama-4", "qwen3", "qwen-2.5-72b", "deepseek-chat", "deepseek-r1", "gemma-3-27b", "mistral-small", "nemotron"]


def free_model():
    """Išrenka veikiantį nemokamą (:free) OpenRouter modelį pagal pirmenybių sąrašą."""
    try:
        with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as r:
            ids = [m["id"] for m in json.loads(r.read().decode()).get("data", []) if m["id"].endswith(":free")]
    except Exception as ex:
        print("Modelių sąrašo gauti nepavyko:", ex); return "meta-llama/llama-3.3-70b-instruct:free"
    for pref in PREF:
        for i in ids:
            if pref in i:
                print("Pasirinktas nemokamas modelis:", i); return i
    return ids[0] if ids else "meta-llama/llama-3.3-70b-instruct:free"


def providers():
    out = []
    if os.environ.get("PERPLEXITY_API_KEY"):
        out.append(("perplexity", "https://api.perplexity.ai/chat/completions", os.environ["PERPLEXITY_API_KEY"], "sonar", 0.006))
    if os.environ.get("OPENROUTER_API_KEY"):
        models = os.environ.get("OPENROUTER_MODEL") or free_model()
        for m in [x.strip() for x in models.split(",") if x.strip()]:
            out.append(("openrouter:" + m, "https://openrouter.ai/api/v1/chat/completions", os.environ["OPENROUTER_API_KEY"], m, 0.0 if m.endswith(":free") else 0.006))
    if os.environ.get("GROQ_API_KEY"):
        out.append(("groq", "https://api.groq.com/openai/v1/chat/completions", os.environ["GROQ_API_KEY"], "llama-3.3-70b-versatile", 0.0))
    return out


def domains_of(urls):
    d = []
    for u in urls:
        m = re.match(r"https?://(?:www\.)?([^/]+)", u or "")
        if m:
            d.append(m.group(1).lower())
    return d


def ask(prov, lang, q):
    name, url, key, model, _ = prov
    body = {"model": model, "messages": [{"role": "system", "content": SYS.get(lang, SYS["en"])}, {"role": "user", "content": q}],
            "max_tokens": 700, "temperature": 0.2}
    r = post(url, key, body)
    text = (r.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    cites = list(r.get("citations") or [])
    for sr in r.get("search_results") or []:
        if sr.get("url"):
            cites.append(sr["url"])
    for ann in (r.get("choices") or [{}])[0].get("message", {}).get("annotations") or []:
        u = (ann.get("url_citation") or {}).get("url")
        if u:
            cites.append(u)
    doms = domains_of(cites)
    rank = next((i + 1 for i, d in enumerate(doms) if d.endswith(DOMAIN)), "")
    return {"paminetas": int(bool(MENTION.search(text))), "cituotas": int(bool(rank)), "vieta": rank,
            "saltiniai": " ".join(dict.fromkeys(doms))[:500], "ilgis": len(text)}


def main():
    provs = providers()
    if not provs:
        print("Nėra nė vieno rakto (PERPLEXITY_API_KEY / OPENROUTER_API_KEY / GROQ_API_KEY) – nieko nedarau.")
        return 0
    prompts = list(csv.DictReader(open(os.path.join(HERE, "promptai.csv"), encoding="utf-8")))
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"poslinkis": 0}
    start = st["poslinkis"] % len(prompts)
    batch = [prompts[(start + i) % len(prompts)] for i in range(min(BATCH, len(prompts)))]
    os.makedirs(OUT, exist_ok=True)
    today = datetime.date.today().isoformat()
    fp = os.path.join(OUT, f"{today}.csv")
    new = not os.path.exists(fp)
    spent, done = 0.0, 0
    with open(fp, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["data", "tiekejas", "id", "kalba", "klasteris", "tier", "tikslas", "promptas", "paminetas", "cituotas", "vieta", "saltiniai", "klaida"])
        for row in batch:
            if not provs:
                break
            for prov in provs:
                if spent + prov[4] > MAX_USD:
                    print(f"Pasiekta riba {MAX_USD} $ – stoju."); break
                try:
                    res = ask(prov, row["kalba"], row["promptas"]); err = ""
                except urllib.error.HTTPError as ex:
                    res = {}; err = f"HTTP {ex.code}"
                except Exception as ex:
                    res = {}; err = type(ex).__name__
                spent += prov[4] if not err else 0
                w.writerow([today, prov[0], row["id"], row["kalba"], row["klasteris"], row["tier"], row["tikslas"], row["promptas"],
                            res.get("paminetas", ""), res.get("cituotas", ""), res.get("vieta", ""), res.get("saltiniai", ""), err])
                if err.startswith("HTTP 4") and err not in ("HTTP 429",):
                    print(prov[0], err, "– tiekėjas išjungiamas šiam paleidimui"); provs = [p for p in provs if p is not prov]
                time.sleep(0.4)
            else:
                done += 1
                continue
            break
    st["poslinkis"] = start + done
    st["paskutinis"] = today
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    suvestine()
    print(f"Paklausta promptų: {done}, išleista ~{spent:.2f} $")
    return 0


def suvestine():
    rows = []
    for fn in sorted(os.listdir(OUT)):
        if fn.endswith(".csv"):
            rows += list(csv.DictReader(open(os.path.join(OUT, fn), encoding="utf-8")))
    rows = [r for r in rows if not r["klaida"]]
    if not rows:
        return
    by = defaultdict(lambda: [0, 0, 0])
    comp = Counter()
    for r in rows:
        for k in (("viso", r["tiekejas"]), ("kalba", r["kalba"]), ("tier", r["tier"]), ("klasteris", r["klasteris"])):
            b = by[k]; b[0] += 1; b[1] += int(r["paminetas"] or 0); b[2] += int(r["cituotas"] or 0)
        for d in (r["saltiniai"] or "").split():
            comp[d] += 1
    L = [f"# Peter Bravvo – AEO matavimas", f"Atnaujinta: {datetime.date.today().isoformat()}. Patikrų: {len(rows)}.", "",
         "Paminėtas = atsakymo tekste yra Peter Bravvo / Andrzejewski. Cituotas = tarp šaltinių yra peterbravvo.lt.", ""]
    for grp, title in (("viso", "Pagal tiekėją"), ("kalba", "Pagal kalbą"), ("tier", "Pagal lygį"), ("klasteris", "Pagal temą")):
        L += [f"## {title}", "| | patikrų | paminėtas | cituotas |", "|---|---|---|---|"]
        for (g, k), (n, m, c) in sorted(by.items()):
            if g == grp:
                L.append(f"| {k} | {n} | {m} ({100*m//n} %) | {c} ({100*c//n} %) |")
        L.append("")
    L += ["## Dažniausiai cituojami šaltiniai (konkurentai ir katalogai)", "| domenas | kartų |", "|---|---|"]
    L += [f"| {d} | {n} |" for d, n in comp.most_common(25)]
    open(os.path.join(OUT, "SUVESTINE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
