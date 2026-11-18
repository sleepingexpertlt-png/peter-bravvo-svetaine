# peterbravvo.lt

Statinė svetainė: LT / PL / RU / EN, 40 puslapių, schema.org, hreflang, llms.txt.

- `site/` – tai, kas publikuojama (GitHub Pages, žr. `.github/workflows/pages.yml`).
- `src/` – generatorius: `python3 build2.py` (turinys `turinys.py`, faktai `faktai.json`) → `dist2/`, tada nukopijuoti į `site/`.
- `src/promptai.*` – 1068 AI matomumo promptų bankas.
