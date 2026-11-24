---
name: aktualizuj-strone
description: Zmienia treść strony peterbravvo.lt (ceny, teksty, FAQ, artykuły poradnika, zdjęcia), przebudowuje ją i publikuje. Używaj, gdy Piotr mówi „zmień na stronie”, „nowa cena”, „dodaj zdjęcia”, „dodaj pytanie”, „popraw tekst”.
---

# Aktualizacja strony

1. **Gdzie zmieniać:**
   - ceny, telefon, profile → `src/faktai.json`
   - teksty usług, FAQ usług, UI → `src/turinys.py` (Python; polskie/litewskie cudzysłowy „…” tylko wewnątrz stringów w "…")
   - artykuły poradnika → `src/zinynas/z-*.json` (zapisuj przez Python `json.dump(..., ensure_ascii=False, indent=1)`)
   - zdjęcia → `src/foto/<rodzaj>/` gdzie rodzaj ∈ vestuves, imones, jubiliejai, seimos, jaunimas, miestas, balsas. Przed dodaniem zmniejsz do max 1600 px dłuższego boku i JPG ~80 % (`python3 -c "from PIL import Image..."` albo ffmpeg). Nazwy plików: małe litery, bez spacji. Galeria pojawi się sama na stronie danego rodzaju imprezy.
   Zmieniaj zawsze wszystkie 4 języki (lt, pl, ru, en).
2. `./build.sh` → musi wypisać `Puslapių: 104` (lub więcej po dodaniu artykułów).
3. Sprawdź: `python3 -c "import json,re,glob;[json.loads(re.search(r'<script type=\"application/ld\+json\">(.*?)</script>',open(f).read(),re.S).group(1)) for f in glob.glob('site/**/index.html',recursive=True)];print('schema OK')"`
4. `git add -A && git commit -m "<co zmieniono>" && git push origin main`
5. Publikacja: jeśli Hostinger GIT jest podłączony – gotowe po 1–2 min. Jeśli nie – `cd site && zip -qr ../strona.zip . -x CNAME .nojekyll` i daj Piotrowi instrukcję: hPanel → Menedżer plików → public_html → Prześlij `strona.zip` → Rozpakuj (nadpisz) → usuń zip.
6. Odpowiedz Piotrowi jednym zdaniem: co zmieniono i gdzie to zobaczy.
