# -*- coding: utf-8 -*-
"""Peter Bravvo svetainė v2: viena šventės rūšis = savas fonas, spalvos, šriftas ir tekstai. 4 kalbos.
Paleidimas: python3 build2.py  ->  dist2/ (tikri URL) + preview2.html (vienas failas peržiūrai).
Nuotraukos: įdėkite JPG/WEBP į foto/<segmentas>/ (vestuves, imones, ...) ir paleiskite iš naujo – galerija atsiras pati.
"""
import datetime, glob, html, json, os, re, shutil, urllib.parse
BUILD_DATE = datetime.date.today().isoformat()
from turinys import LANGS, SEGS, SLUG, UI, S, HOME, ABOUT, CONTACT, TEMA, POZ, SUKIS
TH = lambda sg: TEMA.get(sg, sg)

ROOT = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(ROOT, "faktai.json"), encoding="utf-8"))
DOMAIN = "https://peterbravvo.lt"
e = html.escape
TEL, TEL_RAW, EMAIL = F["tel"], F["tel_raw"], F["email"]
WA = "https://wa.me/" + TEL_RAW.lstrip("+")
GBP = F["gbp"]
P_EVE, P_HOUR, DEP = F["price_evening"], F["price_hour"], F["deposit_eur"]
PID, SID, WID = DOMAIN + "/#person", DOMAIN + "/#service", DOMAIN + "/#website"
SAME = [F["profiles"]["instagram"], F["profiles"]["facebook"], F["profiles"]["youtube"], "https://www.youtube.com/@bravvoband5082"]
LANG_NAME = {"lt": "LT", "pl": "PL", "ru": "RU", "en": "EN"}
ROLE_STACK = [("lt", "Renginių vedėjas"), ("pl", "Wodzirej"), ("ru", "Ведущий"), ("en", "Event host")]

# ---------- puslapių sąrašas ----------
PAGES = []
for L in LANGS:
    PAGES.append(dict(id=f"{L}-home", lang=L, key="home", kind="home", seg="visi"))
    for sg in SEGS:
        PAGES.append(dict(id=f"{L}-{sg}", lang=L, key=sg, kind="seg", seg=TH(sg)))
    PAGES.append(dict(id=f"{L}-apie", lang=L, key="apie", kind="about", seg="visi"))
    PAGES.append(dict(id=f"{L}-kontaktai", lang=L, key="kontaktai", kind="contact", seg="visi"))
for p in PAGES:
    p["path"] = SLUG[p["lang"]][p["key"]]
    L, k = p["lang"], p["key"]
    src = HOME[L] if k == "home" else ABOUT[L] if k == "apie" else CONTACT[L] if k == "kontaktai" else S[k][L]
    p["title"], p["desc"] = src["title"], src["desc"]
    p["h1"] = src["h1"]
# ---------- žinynas ----------
ZDIR = os.path.join(ROOT, "zinynas") if os.path.isdir(os.path.join(ROOT, "zinynas")) else os.path.join(os.path.dirname(ROOT), "zinynas")
ZBASE = {"lt": "/zinynas/", "pl": "/pl/poradnik/", "ru": "/ru/sovety/", "en": "/en/guide/"}
ZUI = {
 "lt": dict(hub="Žinynas", hub_t="Žinynas: vestuvės, šventės ir renginiai – Peter Bravvo", hub_d="Patarimai iš 400+ renginių: vestuvių eiga, tradicijos, žaidimai, sveikinimai, dvikalbės šventės, vedėjo pasirinkimas.",
           hub_lead="Patarimai iš daugiau nei 400 pravestų renginių: vestuvių eiga, tradicijos, žaidimai, sveikinimai ir kaip išsirinkti vedėją.", read="Skaityti", more="Daugiau apie šią šventę",
           bot="Klausk žinyno", bot_ph="Pvz.: kiek kainuoja vestuvių vedėjas?", bot_send="Klausti", bot_none="Tikslaus atsakymo neradau. Parašykite Piotrui – atsakys tą pačią arba kitą dieną.", bot_more="Skaityti daugiau", bot_hi="Sveiki! Užduokite klausimą apie vestuves, šventę ar vedėją arba pasirinkite:", bot_wa="Rašyti Piotrui"),
 "pl": dict(hub="Poradnik", hub_t="Poradnik: wesela, przyjęcia i imprezy – Peter Bravvo", hub_d="Porady z 400+ imprez: harmonogram wesela, tradycje, zabawy, życzenia, wesela dwujęzyczne, wybór wodzireja.",
           hub_lead="Porady z ponad 400 poprowadzonych imprez: harmonogram wesela, tradycje, zabawy, życzenia i jak wybrać wodzireja.", read="Czytaj", more="Więcej o tej uroczystości",
           bot="Zapytaj poradnik", bot_ph="Np.: ile kosztuje wodzirej?", bot_send="Zapytaj", bot_none="Nie znalazłem dokładnej odpowiedzi. Napiszcie do Piotra – odpowie tego samego lub następnego dnia.", bot_more="Czytaj więcej", bot_hi="Dzień dobry! Zadajcie pytanie o wesele, przyjęcie albo wodzireja lub wybierzcie:", bot_wa="Napisz do Piotra"),
 "ru": dict(hub="Советы", hub_t="Советы: свадьбы, праздники и мероприятия – Peter Bravvo", hub_d="Советы из 400+ мероприятий: программа свадьбы, традиции, конкурсы, поздравления, двуязычные праздники, выбор ведущего.",
           hub_lead="Советы из более чем 400 проведённых мероприятий: программа свадьбы, традиции, конкурсы, поздравления и как выбрать ведущего.", read="Читать", more="Подробнее об этом празднике",
           bot="Спросите справочник", bot_ph="Например: сколько стоит ведущий на свадьбу?", bot_send="Спросить", bot_none="Точного ответа не нашлось. Напишите Петру – ответит в тот же или на следующий день.", bot_more="Читать подробнее", bot_hi="Здравствуйте! Задайте вопрос о свадьбе, празднике или ведущем или выберите:", bot_wa="Написать Петру"),
 "en": dict(hub="Guide", hub_t="Guide: weddings, parties and events – Peter Bravvo", hub_d="Advice from 400+ events: wedding timeline, traditions, games, toasts, bilingual celebrations and choosing a host.",
           hub_lead="Advice from more than 400 hosted events: wedding timeline, traditions, games, toasts and how to choose a host.", read="Read", more="More about this celebration",
           bot="Ask the guide", bot_ph="E.g. how much does a wedding host cost?", bot_send="Ask", bot_none="I couldn't find an exact answer. Write to Piotr – he replies the same or the next day.", bot_more="Read more", bot_hi="Hi! Ask about a wedding, a party or a host, or pick one:", bot_wa="Message Piotr"),
}
ZART = []
for i, fp in enumerate(sorted(glob.glob(os.path.join(ZDIR, "z-*.json"))), 1):
    try:
        d = json.load(open(fp, encoding="utf-8"))
    except Exception as ex:
        print("SKIP", fp, ex); continue
    if not all(L in d for L in LANGS):
        print("SKIP (kalbos)", fp); continue
    d["key"] = f"z{i:02d}"
    ZART.append(d)
if ZART:
    for L in LANGS:
        PAGES.append(dict(id=f"{L}-zinynas", lang=L, key="zinynas", kind="hub", seg="visi", path=ZBASE[L],
                          title=ZUI[L]["hub_t"], desc=ZUI[L]["hub_d"], h1=ZUI[L]["hub"]))
        for d in ZART:
            a = d[L]
            PAGES.append(dict(id=f"{L}-{d['key']}", lang=L, key=d["key"], kind="art", seg=d.get("segmentas", "visi") if d.get("segmentas") in SEGS else "visi",
                              path=ZBASE[L] + a["slug"].strip("/") + "/", title=a["title"], desc=a["desc"], h1=a["h1"], art=a, zseg=d.get("segmentas")))
BYID = {p["id"]: p for p in PAGES}
LINK = lambda pid: f"@@{pid}@@"
LINKRE = r"@@([a-z]{2}-[a-z0-9]+)@@"


# ---------- blokai ----------
def facts(L):
    return '<dl class="facts">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in UI[L]["facts"]) + "</dl>"


def ctas(L, pid):
    u = UI[L]
    return (f'<div class="ctas"><a class="btn solid" href="tel:{TEL_RAW}">{e(u["call"])} <span class="num">{e(TEL)}</span></a>'
            f'<a class="btn" href="{WA}" rel="noopener">{e(u["wa"])}</a>'
            f'<a class="btn" href="#f-{pid}">{e(u["ask"])}</a></div>')


def chooser(p):
    L, u = p["lang"], UI[p["lang"]]
    items = [("home", "visi", u["all"])] + [(sg, sg, S[sg][L]["chip"]) for sg in SEGS]
    lis = []
    for key, seg, label in items:
        cur = ' aria-current="page"' if p["key"] == key else ""
        lis.append(f'<li><a class="chip" href="{LINK(f"{L}-{key}")}"{cur}><i data-seg="{TH(seg)}"></i>{e(label)}</a></li>')
    return f'<nav class="chooser" aria-label="{e(u["menu"])}"><p class="ch-q">{e(u["chooser"])}</p><ul>{"".join(lis)}</ul></nav>'


def prices(L, hi):
    u = UI[L]
    rows = [("even", u["p_even"], f'{u["from_"]} {P_EVE} €', u["p_even_d"]),
            ("hour", u["p_hour"], f'{P_HOUR} {u["per_h"]}', u["p_hour_d"]),
            ("dep", u["p_dep"], f'{DEP} €', u["p_dep_d"])]
    cells = "".join(f'<div class="price{" hi" if k == hi else ""}"><h3>{e(t)}</h3><p class="amt">{e(a)}</p><p>{e(d)}</p></div>' for k, t, a, d in rows)
    return f'<section class="blk"><h2>{e(u["prices"])}</h2><div class="prices">{cells}</div><p class="note">{e(u["p_note"])}</p></section>'


def steps(L):
    u = UI[L]
    li = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in u["steps"])
    return f'<section class="blk"><h2>{e(u["how"])}</h2><ol class="steps">{li}</ol></section>'


def style_blk(L):
    u = UI[L]
    return (f'<section class="blk style"><h2>{e(u["style_h"])}</h2><ul class="trio">'
            + "".join(f"<li>{e(x)}</li>" for x in u["style"]) + f'</ul><p class="measure">{e(u["style_p"])}</p></section>')


def faq_blk(L, faq):
    u = UI[L]
    d = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    return f'<section class="blk"><h2>{e(u["faq"])}</h2><div class="faq">{d}</div></section>'


def reviews(L):
    u = UI[L]
    return (f'<a class="reviews" href="{GBP}" rel="noopener"><b>{F["google_reviews"]}</b><span>{e(u["reviews_n"])}</span>'
            f'<em>{e(u["reviews"])} →</em></a>')


def press_blk(L, full):
    u = UI[L]
    items = F["press"] if full else [x for x in F["press"] if x["type"] in ("about", "video")][:5]
    li = []
    for x in items:
        kind = "▶ " if x["type"] == "video" else ""
        date = f' · {e(x["date"][:4])}' if x.get("date") else ""
        li.append(f'<li><a href="{e(x["url"])}" rel="noopener">{kind}{e(x["t"])}</a><span>{e(x["src"])}{date}</span></li>')
    return f'<section class="blk"><h2>{e(u["press"])}</h2><ul class="press">{"".join(li)}</ul></section>'


def gallery(seg):
    pics = sorted(glob.glob(os.path.join(ROOT, "foto", seg, "*.jpg")) + glob.glob(os.path.join(ROOT, "foto", seg, "*.webp")))
    if not pics:
        return ""
    figs = "".join(f'<figure><img src="/foto/{seg}/{os.path.basename(x)}" alt="" loading="lazy" decoding="async"></figure>' for x in pics[:9])
    return f'<section class="blk"><div class="gal">{figs}</div></section>'


def form_blk(p, preset):
    L, u, pid = p["lang"], UI[p["lang"]], p["id"]
    opts = "".join(f'<option{" selected" if sg == preset else ""}>{e(S[sg][L]["chip"])}</option>' for sg in SEGS)
    f = lambda n: f"{pid}-{n}"
    return f'''<section class="blk contact" id="f-{pid}"><h2>{e(u["contact"])}</h2>
<div class="direct"><a href="tel:{TEL_RAW}">{e(TEL)}</a><a href="mailto:{EMAIL}">{e(EMAIL)}</a><a href="{WA}" rel="noopener">WhatsApp</a></div>
<form class="ask" action="mailto:{EMAIL}" method="post" enctype="text/plain" data-wa="{WA}" data-mail="{EMAIL}">
<div class="fld"><label for="{f("t")}">{e(u["f_type"])}</label><select id="{f("t")}" name="renginys">{opts}</select></div>
<div class="fld"><label for="{f("d")}">{e(u["f_date"])}</label><input id="{f("d")}" name="data" type="date"></div>
<div class="fld"><label for="{f("v")}">{e(u["f_place"])}</label><input id="{f("v")}" name="vieta" autocomplete="off"></div>
<div class="fld"><label for="{f("g")}">{e(u["f_guests"])}</label><input id="{f("g")}" name="sveciai" inputmode="numeric"></div>
<div class="fld"><label for="{f("n")}">{e(u["f_name"])}</label><input id="{f("n")}" name="vardas" autocomplete="name"></div>
<div class="fld wide"><label for="{f("m")}">{e(u["f_msg"])}</label><textarea id="{f("m")}" name="zinute" rows="3"></textarea></div>
<div class="wide sends"><button class="btn solid" type="submit" value="wa">{e(u["f_wa"])}</button><button class="btn" type="submit" value="mail">{e(u["f_mail"])}</button></div>
<p class="wide note">{e(u["f_note"])}</p></form></section>'''


def segcards(L):
    out = []
    for sg in SEGS:
        s = S[sg][L]
        out.append(f'<a class="segcard" data-seg="{TH(sg)}" href="{LINK(f"{L}-{sg}")}"><span class="sc-k">{e(s["chip"])}</span>'
                   f'<span class="sc-t">{e(s["lead"].split(". ")[0].rstrip("."))}.</span><span class="sc-go">→</span></a>')
    return f'<section class="blk"><div class="segcards">{"".join(out)}</div></section>'


# ---------- puslapio kūnas ----------
def poz_blk(L):
    z = POZ[L]
    return (f'<section class="blk style"><h2>{e(z["h"])}</h2><ul class="trio">' + "".join(f"<li>{e(x)}</li>" for x in z["items"])
            + f'</ul><p class="measure">{e(z["p"])}</p></section>')


# Viešų renginių, kuriuos vedė Peter Bravvo, sąrašas (iš žiniasklaidos; datos tik tiek, kiek žinoma)
EVENTS = [
    dict(name="Joninės Rudaminoje 2024", start="2024-06", place="Rudamina, Vilniaus rajonas", url="https://vrsa.lt/titulinio-naujienos/424/jonines-rudaminoje-koncertas-dj-jovani-ispudingas-lazeriu-sou-ir-sokiai-iki-ryto:4884"),
    dict(name="Kalėdų eglės įžiebimas Nemenčinėje 2019", start="2019", place="Nemenčinė, Vilniaus rajonas", url="https://vilnijosnaujienos.lt/zaliaskare-nusvito-ir-nemencineje/"),
    dict(name="Miss Polka Litwy 2019", start="2019", place="Lietuva", url="https://kurierwilenski.lt/2019/02/18/dominika-lamauskaite-dziewczyna-kuriera-wilenskiego-miss-polka-litwy-2019/"),
]


def events_graph():
    return [{"@type": "Event", "@id": DOMAIN + "/#event-" + str(i), "name": ev["name"], "startDate": ev["start"],
             "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
             "location": {"@type": "Place", "name": ev["place"], "address": {"@type": "PostalAddress", "addressLocality": ev["place"].split(",")[0], "addressCountry": "LT"}},
             "performer": {"@id": PID}, "url": ev["url"]} for i, ev in enumerate(EVENTS, 1)]


def main_of(p):
    L, k, u = p["lang"], p["key"], UI[p["lang"]]
    if p["kind"] == "home":
        return facts(L) + poz_blk(L) + segcards(L) + style_blk(L) + prices(L, "even") + steps(L) + press_blk(L, False) + form_blk(p, "vestuves")
    if p["kind"] == "seg":
        s = S[k][L]
        get = "".join(f"<li>{e(x)}</li>" for x in s["get"])
        body = (facts(L) + f'<section class="blk"><h2>{e(u["get"])}</h2><ul class="get">{get}</ul></section>'
                + f'<p class="proof">{e(s["proof"])}</p>' + gallery(k))
        if s["price"] != "none":
            body += prices(L, s["price"]) + steps(L)
        return body + faq_blk(L, s["faq"]) + form_blk(p, k)
    if p["kind"] == "about":
        paras = "".join(f'<p>{e(x)}</p>' for x in ABOUT[L]["paras"])
        return facts(L) + f'<section class="blk measure prose">{paras}</section>' + style_blk(L) + press_blk(L, True) + form_blk(p, "vestuves")
    if p["kind"] == "hub":
        cards = "".join(f'<a class="segcard" data-seg="{BYID[f"{L}-{d['key']}"]["seg"]}" href="{LINK(f"{L}-{d['key']}")}"><span class="sc-k">{e(d[L]["h1"])}</span>'
                        f'<span class="sc-t">{e(d[L]["desc"])}</span><span class="sc-go">{e(ZUI[L]["read"])} →</span></a>' for d in ZART)
        return f'<section class="blk"><div class="segcards">{cards}</div></section>' + form_blk(p, "vestuves")
    if p["kind"] == "art":
        a = p["art"]
        secs = []
        for sc in a.get("sections", []):
            body = "".join(f"<p>{e(x)}</p>" for x in sc.get("p", []))
            if sc.get("list"):
                body += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in sc["list"]) + "</ul>"
            secs.append(f'<section class="blk prose measure"><h2>{e(sc.get("h2", ""))}</h2>{body}</section>')
        faq = [(x["q"], x["a"]) for x in a.get("faq", [])]
        more = ""
        if p.get("zseg") in SEGS:
            more = f'<p class="proof"><a href="{LINK(f"{L}-{p["zseg"]}")}">{e(ZUI[L]["more"])}: {e(S[p["zseg"]][L]["chip"])} →</a></p>'
        return "".join(secs) + faq_blk(L, faq) + more + form_blk(p, p["zseg"] if p.get("zseg") in SEGS else "vestuves")
    c = CONTACT[L]
    return (f'<section class="blk"><div class="big"><a href="tel:{TEL_RAW}">{e(TEL)}</a><a href="mailto:{EMAIL}">{e(EMAIL)}</a></div>'
            f'<p class="measure">{e(c["need"])}</p><p><a class="btn" href="/peter-bravvo.vcf" download>{e(u["vcard"])}</a></p></section>'
            + form_blk(p, "vestuves") + faq_blk(L, c["faq"]) + prices(L, "even"))


def sukis_of(p):
    k = p["key"] if p["kind"] in ("seg", "home") else None
    if p["kind"] == "art" and p.get("zseg") in SUKIS: k = p["zseg"]
    t = SUKIS.get(k, {}).get(p["lang"]) if k else None
    return f'<p class="sukis">{e(t)}</p>' if t else ""


def lead_of(p):
    L, k = p["lang"], p["key"]
    if k == "home": return HOME[L]["lead"]
    if k == "apie": return ABOUT[L]["paras"][0]
    if k == "kontaktai": return CONTACT[L]["need"]
    if p["kind"] == "hub": return ZUI[L]["hub_lead"]
    if p["kind"] == "art": return p["art"]["answer"]
    return S[k][L]["lead"]


def langs_nav(p):
    out = []
    for L in LANGS:
        cur = ' aria-current="true"' if L == p["lang"] else ""
        out.append(f'<a href="{LINK(f"{L}-{p["key"]}")}" hreflang="{L}" lang="{L}"{cur}>{LANG_NAME[L]}</a>')
    return '<nav class="langs" aria-label="Kalba / Język / Язык / Language">' + "".join(out) + "</nav>"


def section_html(p):
    L, u = p["lang"], UI[p["lang"]]
    roles = "".join(f'<span lang="{l}"{" class=cur" if l == L else ""}>{e(t)}</span>' for l, t in ROLE_STACK)
    zl = f'<a href="{LINK(f"{L}-zinynas")}">{e(ZUI[L]["hub"])}</a>' if ZART else ""
    links = zl + f'<a href="{LINK(f"{L}-apie")}">{e(u["about"])}</a><a href="{LINK(f"{L}-kontaktai")}">{e(u["contacts"])}</a>'
    return f'''<section class="pg" id="v-{p["id"]}" data-seg="{p["seg"]}" data-lang="{L}" lang="{L}">
<header class="top"><a class="mark" href="{LINK(f"{L}-home")}">Peter <b>Bravvo</b></a><div class="topr">{links}{langs_nav(p)}</div></header>
<div class="hero"><canvas class="scene" aria-hidden="true"></canvas><div class="hero-in">
<p class="roles" aria-hidden="true">{roles}</p>
<h1{' class="long"' if len(p['h1'])>30 else ''}>{e(p["h1"])}</h1>{sukis_of(p)}<p class="lead">{e(lead_of(p))}</p>{ctas(L, p["id"])}{reviews(L)}</div></div>
{chooser(p)}
<main class="wrap">{main_of(p)}</main>
<footer class="foot wrap"><p><b>{e(F["brand"])}</b> · {e(u["foot"])}</p><p><a href="tel:{TEL_RAW}">{e(TEL)}</a> · <a href="mailto:{EMAIL}">{e(EMAIL)}</a> · <a href="{F["profiles"]["instagram"]}" rel="noopener">Instagram</a> · <a href="{F["profiles"]["facebook"]}" rel="noopener">Facebook</a> · <a href="{F["profiles"]["youtube"]}" rel="noopener">YouTube</a> · <a href="{GBP}" rel="noopener">Google</a></p></footer>
</section>'''


# ---------- schema.org ----------
JOB = {"lt": "Renginių vedėjas", "pl": "Wodzirej, prowadzący imprezy", "ru": "Ведущий мероприятий", "en": "Event host"}


def graph_for(p):
    L, url = p["lang"], DOMAIN + p["path"]
    person = {"@type": "Person", "@id": PID, "name": F["brand"], "alternateName": F["alt_names"],
              "givenName": "Piotr", "familyName": "Andrzejewski", "url": DOMAIN + "/",
              "jobTitle": [JOB[L], "TV presenter", "Voice-over artist"], "knowsLanguage": F["languages"],
              "homeLocation": {"@type": "City", "name": "Vilnius"},
              "alumniOf": {"@type": "CollegeOrUniversity", "name": "John Paul II Catholic University of Lublin"},
              "sameAs": SAME,
              "subjectOf": [{"@type": "Article" if x["type"] in ("about", "mention") else "CreativeWork", "name": x["t"], "url": x["url"],
                             "publisher": {"@type": "Organization", "name": x["src"]}} for x in F["press"] if x["type"] in ("about", "mention", "project")],
              "contactPoint": {"@type": "ContactPoint", "contactType": "bookings", "telephone": TEL_RAW, "email": EMAIL, "availableLanguage": F["languages"]},
              "description": POZ[L]["h"] + ". " + POZ[L]["p"],
              "knowsAbout": POZ[L]["items"] + [S[sg][L]["chip"] for sg in SEGS],
              "hasOccupation": [{"@type": "Occupation", "name": n, "occupationLocation": {"@type": "City", "name": "Vilnius"}}
                                for n in (JOB[L], S["parodos"][L]["h1"], "TV presenter", "Voice-over artist")],
              "performerIn": [{"@id": DOMAIN + "/#event-" + str(i)} for i in range(1, len(EVENTS) + 1)]}
    offers = [{"@type": "Offer", "priceCurrency": "EUR",
               "priceSpecification": {"@type": "PriceSpecification", "minPrice": P_EVE, "priceCurrency": "EUR"},
               "itemOffered": {"@type": "Service", "name": UI[L]["p_even"] + " – " + UI[L]["p_even_d"]}},
              {"@type": "Offer", "priceCurrency": "EUR",
               "priceSpecification": {"@type": "UnitPriceSpecification", "price": P_HOUR, "priceCurrency": "EUR", "unitCode": "HUR"},
               "itemOffered": {"@type": "Service", "name": UI[L]["p_hour"]}}]
    service = {"@type": "ProfessionalService", "@id": SID, "name": F["brand"], "url": DOMAIN + "/", "founder": {"@id": PID},
               "telephone": TEL_RAW, "email": EMAIL, "priceRange": f"{P_HOUR}–{P_EVE}+ €", "currenciesAccepted": "EUR",
               "areaServed": [{"@type": "City", "name": "Vilnius"}, {"@type": "Country", "name": "Lithuania"}],
               "knowsLanguage": F["languages"], "sameAs": SAME + [GBP],
               "slogan": POZ[L]["h"], "alternateName": POZ[L]["items"], "description": POZ[L]["p"],
               "audience": [{"@type": "PeopleAudience", "audienceType": S[sg][L]["chip"]} for sg in SEGS if sg not in ("parodos", "imones")]
                           + [{"@type": "BusinessAudience", "audienceType": S["parodos"][L]["chip"]}, {"@type": "BusinessAudience", "audienceType": S["imones"][L]["chip"]}],
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": UI[L]["prices"], "itemListElement": offers}}
    website = {"@type": "WebSite", "@id": WID, "url": DOMAIN + "/", "name": F["brand"], "publisher": {"@id": PID}, "inLanguage": LANGS}
    ptype = {"home": "ProfilePage", "about": "AboutPage", "contact": "ContactPage", "hub": "CollectionPage"}.get(p["kind"], "WebPage")
    wp = {"@type": ptype, "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": L,
          "isPartOf": {"@id": WID}, "about": {"@id": PID}}
    if ptype in ("ProfilePage", "AboutPage"):
        wp["mainEntity"] = {"@id": PID}
    g = [person, service, website, wp]
    faq = None
    if p["kind"] == "seg":
        s = S[p["key"]][L]
        sv = {"@type": "Service", "@id": url + "#service", "name": s["h1"], "serviceType": s["chip"], "description": s["desc"],
              "provider": {"@id": PID}, "areaServed": {"@type": "Country", "name": "Lithuania"}, "availableLanguage": F["languages"], "url": url}
        if SUKIS.get(p["key"], {}).get(L):
            sv["slogan"] = SUKIS[p["key"]][L]
        if p["key"] == "vestuves":
            sv["alternateName"] = POZ[L]["items"][:4]
        if p["key"] in ("parodos", "imones"):
            sv["audience"] = {"@type": "BusinessAudience", "audienceType": POZ[L]["items"][4]}
            sv["alternateName"] = POZ[L]["items"][4:]
        if s["price"] == "even":
            sv["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "PriceSpecification", "minPrice": P_EVE, "priceCurrency": "EUR"}}
        elif s["price"] == "hour":
            sv["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": P_HOUR, "priceCurrency": "EUR", "unitCode": "HUR"}}
        wp["mainEntity"] = {"@id": url + "#service"}
        g.append(sv)
        faq = s["faq"]
    elif p["kind"] == "contact":
        faq = CONTACT[L]["faq"]
    elif p["kind"] == "art":
        a = p["art"]
        g.append({"@type": "Article", "@id": url + "#article", "headline": a["h1"][:110], "description": p["desc"], "inLanguage": L,
                  "author": {"@id": PID}, "publisher": {"@id": PID}, "mainEntityOfPage": {"@id": url + "#webpage"},
                  "datePublished": BUILD_DATE, "dateModified": BUILD_DATE, "abstract": a["answer"],
                  "isPartOf": {"@id": DOMAIN + ZBASE[L] + "#webpage"}})
        wp["mainEntity"] = {"@id": url + "#article"}
        faq = [(x["q"], x["a"]) for x in a.get("faq", [])]
    if faq:
        g.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": L,
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if p["kind"] in ("home", "about") or p["key"] in ("miestas", "parodos"):
        g += events_graph()
    if p["kind"] != "home":
        home = BYID[f"{L}-home"]
        items = [{"@type": "ListItem", "position": 1, "name": F["brand"], "item": DOMAIN + home["path"]}]
        if p["kind"] == "art":
            items.append({"@type": "ListItem", "position": 2, "name": ZUI[L]["hub"], "item": DOMAIN + ZBASE[L]})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": p["h1"], "item": url})
        g.append({"@type": "BreadcrumbList", "itemListElement": items})
    return {"@context": "https://schema.org", "@graph": g}


# ---------- stilius ----------
CSS = r"""
/* Idėja: scena keičiasi pagal šventę. Kiekviena šventės rūšis – savas fonas (canvas), spalvos ir antraštės šriftas. */
:root{--bg:#16110d;--ink:#f3ece2;--muted:#b9ad9c;--line:#3a3129;--accent:#e3a54a;--on-accent:#1a120a;--card:#1f1913;
 --fx1:#e3a54a;--fx2:#fff3dc;--fx3:#9b5d2e;--display:"Unbounded",system-ui,sans-serif;--body:"Manrope",system-ui,sans-serif;
 --dw:600;--dls:-.01em;color-scheme:dark}
[data-seg="vestuves"]{--bg:#f6f1e8;--ink:#221d17;--muted:#6c6155;--line:#e0d5c3;--accent:#7f6230;--on-accent:#fffaf0;--card:#fffcf6;
 --fx1:#c9a45c;--fx2:#eadbb8;--fx3:#ffffff;--display:"Cormorant Garamond",Georgia,serif;--dw:600;--dls:0;color-scheme:light}
[data-seg="imones"]{--bg:#0d1624;--ink:#e9eef6;--muted:#9fb0c7;--line:#26354c;--accent:#7cc8e0;--on-accent:#06121c;--card:#132033;
 --fx1:#7cc8e0;--fx2:#3b5f86;--fx3:#d6e6f5;--display:"Unbounded",system-ui,sans-serif;--dw:500;--dls:-.02em;color-scheme:dark}
[data-seg="jubiliejai"]{--bg:#2a0f17;--ink:#f8ebe6;--muted:#d2aea8;--line:#4b2531;--accent:#f0c987;--on-accent:#2a0f17;--card:#35141f;
 --fx1:#f0c987;--fx2:#fff1d6;--fx3:#b9806a;--display:"Cormorant Garamond",Georgia,serif;--dw:600;--dls:0;color-scheme:dark}
[data-seg="seimos"]{--bg:#f2f5f0;--ink:#1e2a23;--muted:#56665c;--line:#d5e0d7;--accent:#b4473b;--on-accent:#ffffff;--card:#ffffff;
 --fx1:#f2a8a0;--fx2:#9fd0bd;--fx3:#f5d48a;--display:"Unbounded",system-ui,sans-serif;--dw:500;--dls:-.01em;color-scheme:light}
[data-seg="jaunimas"]{--bg:#0b0b11;--ink:#f4f4f7;--muted:#a8a8b8;--line:#2a2a37;--accent:#ff4f9e;--on-accent:#0b0b11;--card:#15151d;
 --fx1:#ff4f9e;--fx2:#ffd23f;--fx3:#4fe0ff;--display:"Unbounded",system-ui,sans-serif;--dw:800;--dls:-.03em;color-scheme:dark}
[data-seg="miestas"]{--bg:#090c13;--ink:#f1f3f7;--muted:#a3acbf;--line:#252f43;--accent:#ffb547;--on-accent:#140c00;--card:#111726;
 --fx1:#ffcf7a;--fx2:#6c7cff;--fx3:#ffffff;--display:"Unbounded",system-ui,sans-serif;--dw:700;--dls:-.02em;color-scheme:dark}
[data-seg="balsas"]{--bg:#141414;--ink:#f0eee9;--muted:#aaa59c;--line:#323232;--accent:#ff7a59;--on-accent:#1b0a05;--card:#1d1d1d;
 --fx1:#ff7a59;--fx2:#ffb199;--fx3:#5a5a5a;--display:"Unbounded",system-ui,sans-serif;--dw:500;--dls:-.02em;color-scheme:dark}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--body);transition:background .5s,color .5s}
.pg{background:var(--bg);color:var(--ink)}
a{color:inherit}
img{max-width:100%;display:block}
h1,h2,h3{text-wrap:balance}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}

.top{position:relative;z-index:3;max-width:1080px;margin:0 auto;padding:18px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.mark{font:400 18px/1 "Unbounded",sans-serif;letter-spacing:-.02em;text-decoration:none}
.mark b{font-weight:700;color:var(--accent)}
.topr{display:flex;gap:18px;align-items:center;flex-wrap:wrap;font-size:14px}
.topr>a{text-decoration:none;color:var(--muted)}.topr>a:hover{color:var(--ink)}
.langs{display:flex;gap:2px;border:1px solid var(--line);border-radius:99px;padding:3px}
.langs a{font:600 12px/1 var(--body);letter-spacing:.06em;text-decoration:none;padding:6px 9px;border-radius:99px;color:var(--muted)}
.langs a[aria-current]{background:var(--accent);color:var(--on-accent)}

.hero{position:relative;overflow:hidden;margin-top:-62px;padding:110px 0 56px;isolation:isolate}
.scene{position:absolute;inset:0;width:100%;height:100%;z-index:-2}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 35%,transparent) 0%,color-mix(in srgb,var(--bg) 55%,transparent) 55%,var(--bg) 100%)}
.hero-in{max-width:1080px;margin:0 auto;padding:0 20px}
.roles{display:flex;flex-wrap:wrap;gap:6px 16px;margin:0 0 18px;font:600 12px/1.2 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.roles span.cur{color:var(--accent)}
h1{font-family:var(--display);font-weight:var(--dw);letter-spacing:var(--dls);font-size:clamp(38px,7.2vw,84px);line-height:1.02;margin:0 0 20px;max-width:15ch}
[data-seg="vestuves"] h1,[data-seg="jubiliejai"] h1{font-size:clamp(46px,8.4vw,100px);font-style:italic;line-height:.98}
.sukis{font-family:var(--display);font-style:italic;font-size:clamp(20px,2.6vw,28px);line-height:1.3;color:var(--accent);margin:-6px 0 18px;max-width:34ch}
.lead{font-size:clamp(18px,2.1vw,21px);max-width:58ch;margin:0 0 26px;color:var(--ink)}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px}
.btn{display:inline-flex;align-items:center;gap:8px;font:700 15px/1 var(--body);padding:14px 20px;border-radius:99px;border:1.5px solid var(--accent);color:var(--ink);text-decoration:none;background:transparent;cursor:pointer;transition:transform .15s,background .2s}
.btn:hover{transform:translateY(-1px)}
.btn.solid{background:var(--accent);color:var(--on-accent)}
.btn .num{font-weight:500;opacity:.85}
.reviews{display:inline-flex;align-items:baseline;gap:8px;text-decoration:none;color:var(--muted);font-size:14px}
.reviews b{font:700 22px/1 var(--display);color:var(--ink)}
.reviews em{font-style:normal;text-decoration:underline;text-underline-offset:3px}

.chooser{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-block:1px solid var(--line)}
.chooser .ch-q{max-width:1080px;margin:0 auto;padding:10px 20px 0;font:600 12px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.chooser ul{list-style:none;max-width:1080px;margin:0 auto;padding:8px 20px 12px;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none}
.chooser ul::-webkit-scrollbar{display:none}
.chip{flex:none;display:inline-flex;align-items:center;gap:8px;white-space:nowrap;font:600 14px/1 var(--body);padding:10px 14px;border-radius:99px;border:1px solid var(--line);text-decoration:none;color:var(--ink);background:transparent}
.chip i{width:10px;height:10px;border-radius:50%;background:var(--fx1);flex:none}
.chip[aria-current]{border-color:var(--accent);background:var(--accent);color:var(--on-accent)}
.chip:hover{border-color:var(--accent)}
.chip[aria-current] i{outline:2px solid currentColor;outline-offset:1px}
@media (min-width:821px){.chooser ul{flex-wrap:wrap;overflow:visible}}
.facts+.blk{border-top:0}
h1.long{font-size:clamp(34px,5.4vw,64px)}

main{padding-top:8px}
.blk{padding:44px 0;border-top:1px solid var(--line)}
.blk h2{font-family:var(--display);font-weight:var(--dw);letter-spacing:var(--dls);font-size:clamp(26px,3.6vw,40px);line-height:1.1;margin:0 0 22px}
[data-seg="vestuves"] .blk h2,[data-seg="jubiliejai"] .blk h2{font-size:clamp(32px,4.4vw,50px)}
.measure{max-width:64ch}
.prose p{margin:0 0 16px}
.facts{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin:28px 0 8px;border-block:1px solid var(--line)}
.facts div{padding:16px 14px 16px 0}
.facts dt{font:700 22px/1.15 var(--display);font-variant-numeric:tabular-nums;color:var(--ink)}
[data-seg="vestuves"] .facts dt,[data-seg="jubiliejai"] .facts dt{font-size:30px}
.facts dd{margin:4px 0 0;font-size:13px;color:var(--muted)}
.get{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.get li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 18px 46px;position:relative}
.get li::before{content:"";position:absolute;left:18px;top:25px;width:12px;height:12px;border-radius:50%;background:var(--accent)}
.proof{font-family:var(--display);font-size:clamp(20px,2.4vw,26px);line-height:1.35;margin:0;padding:34px 0;border-top:1px solid var(--line);max-width:46ch}
[data-seg="vestuves"] .proof,[data-seg="jubiliejai"] .proof{font-style:italic;font-size:clamp(24px,2.8vw,32px)}
.segcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.segcard{display:flex;flex-direction:column;gap:10px;min-height:190px;padding:20px;border-radius:16px;background:var(--bg);color:var(--ink);border:1px solid var(--line);text-decoration:none;position:relative;overflow:hidden;transition:transform .2s}
.segcard:hover{transform:translateY(-3px)}
.segcard::after{content:"";position:absolute;right:-30px;top:-30px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,var(--fx1),transparent 70%);opacity:.55}
.sc-k{font:var(--dw) 21px/1.15 var(--display);letter-spacing:var(--dls);position:relative;z-index:1}
[data-seg="vestuves"].segcard .sc-k,[data-seg="jubiliejai"].segcard .sc-k{font-size:27px;font-style:italic}
.sc-t{font-size:14px;color:var(--muted);flex:1}
.sc-go{color:var(--accent);font-weight:700}
.trio{list-style:none;margin:0 0 18px;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.trio li{font:600 15px/1 var(--body);padding:12px 16px;border-radius:99px;background:var(--card);border:1px solid var(--line)}
.prices{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.price{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}
.price.hi{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.price h3{margin:0;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.price .amt{font:var(--dw) 30px/1.1 var(--display);margin:10px 0 6px;font-variant-numeric:tabular-nums}
.price p{margin:0;font-size:14px;color:var(--muted)}
.note{font-size:14px;color:var(--muted);margin:14px 0 0}
.steps{list-style:none;counter-reset:s;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.steps li{counter-increment:s;border-top:2px solid var(--accent);padding-top:14px}
.steps li::before{content:counter(s);font:700 13px/1 var(--body);color:var(--accent)}
.steps h3{font-size:17px;margin:8px 0 6px}.steps p{margin:0;font-size:15px;color:var(--muted)}
.faq details{border-bottom:1px solid var(--line);padding:4px 0}
.faq summary{cursor:pointer;font-weight:700;padding:14px 0;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::after{content:"+";color:var(--accent);font-size:22px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq p{margin:0 0 16px;color:var(--muted);max-width:64ch}
.press{list-style:none;margin:0;padding:0;columns:2;column-gap:28px}
.press li{break-inside:avoid;padding:10px 0;border-bottom:1px solid var(--line)}
.press a{font-weight:600;text-decoration:none}.press a:hover{text-decoration:underline}
.press span{display:block;font-size:13px;color:var(--muted)}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.gal img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:10px}
.contact .direct{display:flex;flex-wrap:wrap;gap:8px 22px;margin:0 0 22px;font:600 18px/1.3 var(--body)}
.big{display:flex;flex-direction:column;gap:6px;margin-bottom:16px}
.big a{font:var(--dw) clamp(26px,4.6vw,46px)/1.15 var(--display);text-decoration:none;word-break:break-word}
.ask{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;max-width:760px}
.fld{display:flex;flex-direction:column;gap:6px}.ask label{font-size:13px;font-weight:700;color:var(--muted)}
.ask input,.ask select,.ask textarea{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;width:100%}
.ask .wide{grid-column:1/-1}
.ask label:nth-of-type(odd):not(.wide){grid-column:1}.ask label:nth-of-type(even){grid-column:2}
.sends{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.foot{padding:32px 20px 48px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.foot a{color:var(--muted)}
.banner{background:#1d1d1d;color:#f5d48a;font:600 13px/1.2 system-ui,sans-serif;text-align:center;padding:8px 12px;position:relative;z-index:9}

/* forma: etiketė virš lauko, poromis */
@media (max-width:820px){.facts{grid-template-columns:repeat(2,1fr)}.facts div:last-child{grid-column:1/-1}.steps{grid-template-columns:repeat(2,1fr)}.prices{grid-template-columns:1fr}.press{columns:1}}
@media (max-width:560px){body{font-size:16px}.get{grid-template-columns:1fr}.steps{grid-template-columns:1fr}.ask{grid-template-columns:1fr}.gal{grid-template-columns:repeat(2,1fr)}.hero{padding:100px 0 40px}.topr>a{display:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
@view-transition{navigation:auto}
"""

# Forma: pora etikečių ir laukų dviem stulpeliais – paprasčiau grupėmis
CSS = CSS.replace(".ask label:nth-of-type(odd):not(.wide){grid-column:1}.ask label:nth-of-type(even){grid-column:2}\n", "")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,500;1,600&family=Manrope:wght@400;600;700&family=Unbounded:wght@400;500;600;700;800&display=swap">')

# ---------- JS: fonų scenos + forma ----------
JS = r"""
(function(){
var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
function rnd(a,b){return a+Math.random()*(b-a)}
function col(el,n){return getComputedStyle(el).getPropertyValue(n).trim()||'#fff'}
var SCENES={
 visi:function(c,W,H){var P=[];for(var i=0;i<60;i++)P.push({x:rnd(0,W),y:rnd(0,H),r:rnd(.6,2),v:rnd(.05,.25)});
  return function(t){c.clearRect(0,0,W,H);var a=col(c.canvas,'--fx1');
   for(var k=0;k<3;k++){var cx=W*(.2+.3*k)+Math.sin(t/2600+k*2)*W*.08;var g=c.createLinearGradient(cx,0,cx,H);g.addColorStop(0,a+'55');g.addColorStop(1,a+'00');
    c.fillStyle=g;c.beginPath();c.moveTo(cx-14,0);c.lineTo(cx+14,0);c.lineTo(cx+W*.16,H);c.lineTo(cx-W*.16,H);c.closePath();c.fill();}
   c.fillStyle=col(c.canvas,'--fx2');P.forEach(function(p){p.y-=p.v;if(p.y<0)p.y=H;c.globalAlpha=.35;c.beginPath();c.arc(p.x,p.y,p.r,0,7);c.fill();});c.globalAlpha=1;}},
 vestuves:function(c,W,H){var P=[];for(var i=0;i<34;i++)P.push({x:rnd(0,W),y:rnd(0,H),r:rnd(8,46),v:rnd(.08,.3),a:rnd(.12,.4),k:i%2});
  return function(t){c.clearRect(0,0,W,H);var a=[col(c.canvas,'--fx1'),col(c.canvas,'--fx2')];
   P.forEach(function(p){p.y-=p.v;if(p.y<-p.r)p.y=H+p.r;var x=p.x+Math.sin(t/3000+p.r)*8;var g=c.createRadialGradient(x,p.y,0,x,p.y,p.r);
    g.addColorStop(0,a[p.k]);g.addColorStop(1,a[p.k]+'00');c.globalAlpha=p.a;c.fillStyle=g;c.beginPath();c.arc(x,p.y,p.r,0,7);c.fill();});c.globalAlpha=1;}},
 imones:function(c,W,H){var L=[];for(var i=0;i<26;i++)L.push({x:(i+.5)*W/26,o:rnd(0,1),v:rnd(.0006,.0016)});
  return function(t){c.clearRect(0,0,W,H);c.strokeStyle=col(c.canvas,'--fx2');c.globalAlpha=.35;c.lineWidth=1;
   L.forEach(function(l){c.beginPath();c.moveTo(l.x,0);c.lineTo(l.x,H);c.stroke();});
   c.globalAlpha=1;var a=col(c.canvas,'--fx1');L.forEach(function(l){var y=((t*l.v+l.o)%1.2)*H;var g=c.createLinearGradient(0,y-90,0,y);g.addColorStop(0,a+'00');g.addColorStop(1,a);
    c.strokeStyle=g;c.lineWidth=2;c.beginPath();c.moveTo(l.x,y-90);c.lineTo(l.x,y);c.stroke();});}},
 jubiliejai:function(c,W,H){var P=[];for(var i=0;i<70;i++)P.push({x:rnd(0,W),y:rnd(0,H),r:rnd(1.5,6),v:rnd(.2,.8)});
  return function(t){c.clearRect(0,0,W,H);c.strokeStyle=col(c.canvas,'--fx1');c.lineWidth=1.2;
   P.forEach(function(p){p.y-=p.v;if(p.y<-8){p.y=H+8;p.x=rnd(0,W)}var x=p.x+Math.sin(t/700+p.y/40)*2;c.globalAlpha=.55;c.beginPath();c.arc(x,p.y,p.r,0,7);c.stroke();});c.globalAlpha=1;}},
 seimos:function(c,W,H){var P=[];for(var i=0;i<16;i++)P.push({x:rnd(0,W),y:rnd(H*.15,H*.9),r:rnd(18,40),k:i%3,ph:rnd(0,6)});
  return function(t){c.clearRect(0,0,W,H);var cs=[col(c.canvas,'--fx1'),col(c.canvas,'--fx2'),col(c.canvas,'--fx3')];
   P.forEach(function(p){var y=p.y+Math.sin(t/1400+p.ph)*10,x=p.x+Math.cos(t/1900+p.ph)*6;c.globalAlpha=.5;
    c.strokeStyle=cs[p.k];c.lineWidth=1;c.beginPath();c.moveTo(x,y+p.r*1.15);c.quadraticCurveTo(x+8,y+p.r*1.8,x,y+p.r*2.6);c.stroke();
    c.fillStyle=cs[p.k];c.beginPath();c.ellipse(x,y,p.r*.86,p.r,0,0,7);c.fill();});c.globalAlpha=1;}},
 jaunimas:function(c,W,H){var P=[];for(var i=0;i<90;i++)P.push({x:rnd(0,W),y:rnd(-H,H),w:rnd(4,10),h:rnd(8,18),v:rnd(.6,1.8),r:rnd(0,6),s:rnd(-.05,.05),k:i%3});
  return function(t){c.clearRect(0,0,W,H);var cs=[col(c.canvas,'--fx1'),col(c.canvas,'--fx2'),col(c.canvas,'--fx3')];
   P.forEach(function(p){p.y+=p.v;p.r+=p.s;if(p.y>H+20){p.y=-20;p.x=rnd(0,W)}c.save();c.translate(p.x+Math.sin(t/900+p.r)*6,p.y);c.rotate(p.r);
    c.globalAlpha=.8;c.fillStyle=cs[p.k];c.fillRect(-p.w/2,-p.h/2,p.w,p.h*Math.abs(Math.cos(p.r*1.3))+1);c.restore();});c.globalAlpha=1;}},
 miestas:function(c,W,H){return function(t){c.clearRect(0,0,W,H);var cs=[col(c.canvas,'--fx1'),col(c.canvas,'--fx2'),col(c.canvas,'--fx1')];
   for(var k=0;k<5;k++){var bx=W*(.1+.2*k),ang=Math.sin(t/2200+k*1.7)*.5-Math.PI/2,len=H*1.4,sp=.11;var a=cs[k%3];
    var g=c.createLinearGradient(bx,H,bx+Math.cos(ang)*len,H+Math.sin(ang)*len);g.addColorStop(0,a+'88');g.addColorStop(1,a+'00');c.fillStyle=g;
    c.beginPath();c.moveTo(bx,H);c.lineTo(bx+Math.cos(ang-sp)*len,H+Math.sin(ang-sp)*len);c.lineTo(bx+Math.cos(ang+sp)*len,H+Math.sin(ang+sp)*len);c.closePath();c.fill();}}},
 balsas:function(c,W,H){return function(t){c.clearRect(0,0,W,H);var cs=[col(c.canvas,'--fx1'),col(c.canvas,'--fx2'),col(c.canvas,'--fx3')];
   for(var k=0;k<3;k++){c.strokeStyle=cs[k];c.globalAlpha=k?.45:.9;c.lineWidth=k?1.2:2;c.beginPath();
    for(var x=0;x<=W;x+=4){var env=Math.sin(Math.PI*x/W);var y=H*.55+Math.sin(x/(38+k*14)+t/(420+k*160))*env*(H*.16)*(0.6+0.4*Math.sin(t/900+x/180));x?c.lineTo(x,y):c.moveTo(x,y);}
    c.stroke();}c.globalAlpha=1;}}
};
var cur=null,raf=0;
function start(sec){
 cancelAnimationFrame(raf);var cv=sec&&sec.querySelector('canvas.scene');if(!cv)return;
 var seg=sec.getAttribute('data-seg')||'visi',dpr=Math.min(window.devicePixelRatio||1,2);
 var r=cv.getBoundingClientRect(),W=Math.max(1,r.width),H=Math.max(1,r.height);cv.width=W*dpr;cv.height=H*dpr;
 var c=cv.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);var draw=(SCENES[seg]||SCENES.visi)(c,W,H);cur=sec;
 if(RM){draw(4000);return}
 var t0=performance.now();(function loop(now){if(!document.hidden)draw(now-t0+4000);raf=requestAnimationFrame(loop)})(t0);
}
window.PBscene=start;
var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){start(cur)},200)});

document.addEventListener('submit',function(ev){var f=ev.target;if(!f.classList||!f.classList.contains('ask'))return;ev.preventDefault();
 var mode=(ev.submitter&&ev.submitter.value)||'wa',lines=[];
 f.querySelectorAll('input,select,textarea').forEach(function(x){var lab=f.querySelector('label[for="'+x.id+'"]');if(x.value)lines.push((lab?lab.textContent:x.name)+': '+x.value)});
 var txt=lines.join('\n')||'Labas!';
 if(mode==='mail'){location.href='mailto:'+f.getAttribute('data-mail')+'?subject='+encodeURIComponent('Peter Bravvo')+'&body='+encodeURIComponent(txt)}
 else{window.open(f.getAttribute('data-wa')+'?text='+encodeURIComponent(txt),'_blank','noopener')}
});
})();
"""

PREVIEW_JS = r"""
(function(){
function show(){var id=(location.hash||'#lt-home').slice(1);var sec=document.getElementById('v-'+id);
 if(!sec){var f=document.getElementById('f-'+id.replace(/^f-/,''));if(f&&id.indexOf('f-')===0){f.scrollIntoView();return}sec=document.getElementById('v-lt-home')}
 document.querySelectorAll('.pg').forEach(function(s){s.hidden=s!==sec});
 document.documentElement.setAttribute('data-seg',sec.getAttribute('data-seg'));document.documentElement.lang=sec.getAttribute('data-lang');
 document.title=sec.getAttribute('data-title');window.scrollTo(0,0);window.PBscene&&window.PBscene(sec);}
addEventListener('hashchange',show);show();
})();
"""


def relpre(path):
    depth = len([x for x in path.strip("/").split("/") if x])
    return "../" * depth or "./"


def to_static(s, path="/"):
    pre = relpre(path)
    def f(m):
        t = BYID[m.group(1)]["path"].lstrip("/")
        return (pre + t) if t else pre
    s = re.sub(LINKRE, f, s)
    return s.replace('href="/peter-bravvo.vcf"', f'href="{pre}peter-bravvo.vcf"')


def to_hash(s):
    return re.sub(LINKRE, lambda m: "#" + m.group(1), s)


VERIF = {}
_vf = os.path.join(ROOT, "patvirtinimai.txt")  # eilutės: google=XXXX / bing=YYYY
if os.path.exists(_vf):
    for ln in open(_vf, encoding="utf-8"):
        if "=" in ln:
            k, v = ln.strip().split("=", 1); VERIF[k.strip()] = v.strip()


def head_common():
    v = ""
    if VERIF.get("google"): v += f'<meta name="google-site-verification" content="{e(VERIF["google"])}">'
    if VERIF.get("bing"): v += f'<meta name="msvalidate.01" content="{e(VERIF["bing"])}">'
    return '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + v + FONTS


def alternates(p):
    out = []
    for L in LANGS:
        out.append(f'<link rel="alternate" hreflang="{L}" href="{DOMAIN}{BYID[f"{L}-{p["key"]}"]["path"]}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{BYID["lt-" + p["key"]]["path"]}">')
    return "".join(out)


def render_static(p):
    url = DOMAIN + p["path"]
    og_loc = {"lt": "lt_LT", "pl": "pl_PL", "ru": "ru_RU", "en": "en_GB"}[p["lang"]]
    sec = section_html(p).replace('<section class="pg"', '<div class="pg"', 1)
    sec = sec[: sec.rfind("</section>")] + "</div>"
    body = to_static(sec, p["path"])
    return f'''<!DOCTYPE html><html lang="{p["lang"]}" data-seg="{p["seg"]}"><head>{head_common()}
<title>{e(p["title"])}</title><meta name="description" content="{e(p["desc"])}"><link rel="canonical" href="{url}">{alternates(p)}
<meta property="og:type" content="{"article" if p["kind"] == "art" else "profile"}"><meta property="og:title" content="{e(p["title"])}"><meta property="og:description" content="{e(p["desc"])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{og_loc}">
<script type="application/ld+json">{json.dumps(graph_for(p), ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<a class="skip" href="#f-{p["id"]}" style="position:absolute;left:-9999px">{e(UI[p["lang"]]["skip"])}</a>
{body}
<script>{JS}window.PBscene(document.querySelector('.pg'));</script></body></html>'''


def render_preview():
    secs = []
    for p in PAGES:
        s = to_hash(section_html(p)).replace('href="/peter-bravvo.vcf"', 'href="data:text/vcard;charset=utf-8,' + urllib.parse.quote(VCF) + '"')
        s = s.replace(f'id="v-{p["id"]}"', f'id="v-{p["id"]}" data-title="{e(p["title"])}"', 1)
        # nuotraukos peržiūroje nerodomos (jų dar nėra)
        secs.append(s)
    return f'''<!DOCTYPE html><html lang="lt" data-seg="visi"><head>{head_common()}<title>Peter Bravvo svetainė</title>
<style>{CSS}</style></head><body><div class="banner">{e(UI["lt"]["banner"])}</div>
{"".join(secs)}
<script>{JS}</script><script>{PREVIEW_JS}</script></body></html>'''


ROBOTS = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {D}/sitemap.xml
"""


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in PAGES:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{L}" href="{DOMAIN}{BYID[f"{L}-{p["key"]}"]["path"]}"/>' for L in LANGS)
        out.append(f"<url><loc>{DOMAIN}{p['path']}</loc>{alts}</url>")
    out.append("</urlset>")
    return "\n".join(out)


def llms():
    L = "lt"
    lines = [f"# {F['brand']}", "",
             f"> {F['brand']} (Piotr Andrzejewski / Piotras Andžejevskis) – renginių vedėjas iš Vilniaus. Veda lietuvių, lenkų, rusų ir anglų kalbomis. 400+ renginių, 150+ vestuvių (nuo 2013 m.). 2021–2023 m. laidos „Co się dzieje“ vedėjas TVP Wilno. Nuo 2021 m. balso aktorius Rygos studijoje Digi Media (TV anonsai, įskaitant Nickelodeon kanalą).",
             "", "Pozicionavimas: " + " · ".join(POZ["lt"]["items"]) + ".",
             "", f"Kontaktai: {TEL}, {EMAIL}. Kainos: vakaro programa nuo {P_EVE} €, konferansas {P_HOUR} €/val., avansas {DEP} €.", "", "## Puslapiai"]
    for p in PAGES:
        lines.append(f"- [{p['title']}]({DOMAIN}{p['path']}): {p['desc']}")
    lines += ["", "## Šaltiniai"] + [f"- [{x['t']}]({x['url']}) – {x['src']}" for x in F["press"]]
    return "\n".join(lines) + "\n"


HTACCESS = """ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
"""


def llms_full():
    out = [llms(), "", "# Klausimai ir atsakymai / Pytania i odpowiedzi / Вопросы и ответы / Questions and answers", ""]
    for p in PAGES:
        L = p["lang"]
        qa = []
        if p["kind"] == "seg": qa = S[p["key"]][L]["faq"]
        elif p["kind"] == "contact": qa = CONTACT[L]["faq"]
        elif p["kind"] == "art":
            qa = [(x["q"], x["a"]) for x in p["art"].get("faq", [])]
            out += [f"## {p['h1']} ({L})", f"Šaltinis: {DOMAIN}{p['path']}", "", p["art"]["answer"], ""]
        elif p["kind"] == "home":
            out += [f"## {p['h1']} ({L})", f"Šaltinis: {DOMAIN}{p['path']}", "", HOME[L]["lead"], ""]
        if qa and p["kind"] != "art":
            out += [f"## {p['h1']} ({L})", f"Šaltinis: {DOMAIN}{p['path']}", ""]
        for q, a in qa:
            out += [f"Q: {q}", f"A: {a}", ""]
    return "\n".join(out) + "\n"


VCF = f"""BEGIN:VCARD
VERSION:3.0
N:Andrzejewski;Piotr;;;
FN:Peter Bravvo
ORG:Peter Bravvo
TITLE:Renginių vedėjas / Wodzirej / Ведущий / Event host
TEL;TYPE=CELL:{TEL_RAW}
EMAIL:{EMAIL}
URL:{DOMAIN}/
NOTE:LT / PL / RU / EN
END:VCARD
"""


def build():
    dist = os.path.join(ROOT, "dist2")
    shutil.rmtree(dist, ignore_errors=True)
    for p in PAGES:
        d = os.path.join(dist, p["path"].strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render_static(p))
    if os.path.isdir(os.path.join(ROOT, "foto")):
        shutil.copytree(os.path.join(ROOT, "foto"), os.path.join(dist, "foto"))
    open(os.path.join(dist, "robots.txt"), "w").write(ROBOTS.replace("{D}", DOMAIN))
    open(os.path.join(dist, "sitemap.xml"), "w").write(sitemap())
    open(os.path.join(dist, "llms.txt"), "w", encoding="utf-8").write(llms())
    open(os.path.join(dist, "llms-full.txt"), "w", encoding="utf-8").write(llms_full())
    open(os.path.join(dist, ".htaccess"), "w").write(HTACCESS)
    open(os.path.join(dist, "peter-bravvo.vcf"), "w", encoding="utf-8").write(VCF)
    open(os.path.join(ROOT, "preview2.html"), "w", encoding="utf-8").write(render_preview())
    print("pages", len(PAGES))


if __name__ == "__main__":
    build()
