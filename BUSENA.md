# Peter Bravvo projektas – būsena ir atviri punktai
Atnaujinta 2026-11-24. Užduotis ATVIRA (savininkas: „palikime atvirą“).

## Padaryta ✅
- peterbravvo.lt VEIKIA (Hostinger, Piotro paskyra andzejevskis@gmail.com; savininkas – bendradarbis). 104 puslapiai: 10 puslapių × 4 kalbos + žinynas 15 straipsnių × 4 kalbos (LT /zinynas/, PL /pl/poradnik/, RU /ru/sovety/, EN /en/guide/).
- Schema: Person, ProfessionalService, Service, Article, FAQPage, BreadcrumbList, CollectionPage; hreflang; sitemap (104); robots (AI botai leidžiami); llms.txt + llms-full.txt; .htaccess (https, be www).
- Įkelta į Hostinger ranka (zip), 2026-11-24. Hostinger GIT bendradarbiui NEleidžiamas – jungti turi Piotras pats.
- GitHub: sleepingexpertlt-png/peter-bravvo-svetaine (public). Šaka `hostinger` = svetainės failai šaknyje, atnaujinama automatiškai po push į main.
- AEO botas (`aeo/`): kasdien 08:17 LT, 45 promptai, nemokamas OpenRouter modelis (auto parenka, 11-24: nvidia/nemotron-3.5-super-vl:free), sekretas OPENROUTER_API_KEY įdėtas. Bazė 11-24: 0/5 paminėjimų.
- 1068 promptų bankas: aeo/promptai.csv + Google Sheet 1q3Hl52FgThf-rgVKSk_6Mj0nBtDshCMACAh7kzkffCM.
- Agentas Piotrui: CLAUDE.md (PL) + .claude/skills (post-social, aktualizuj-strone, raport-aeo), build.sh.
- Insta/FB paketas: soc/INSTA_FB_PAKETAS.md + Google Doc 1MIU0nKTcu2yX92lrPZzWluOtufB0SdS6FU3gDhvZdmE (pasidalinta su Piotru).
- Drive aplankas „Peter Bravo – projektas“ 1BM7YQnxF_Y4EGWw5SYSWC-PGSV_CcB55; nuotraukų aplankas 1_z6FzgCqBnXB6j2ZTQ4X05giKiKp7Dxf (pasidalinta su abiem Piotro el. paštais).

## Atvira ⏳
| # | Kas | Kas daro | Būsena |
|---|---|---|---|
| 1 | Nuotraukos (5–10 kiekvienai šventei) → Drive aplankas → `src/foto/<segmentas>/` → galerijos | Piotras įkelia, agentas sudeda | aplankas tuščias 11-24 |
| 2 | Google Search Console: HTML žyma → įdėti į svetainę → sitemap; Bing per GSC importą | savininkas atsiunčia žymą | laukiama |
| 3 | Google verslo profilyje svetainė = https://peterbravvo.lt | Piotras / savininkas | nepadaryta |
| 4 | Insta/FB profiliai pagal paketą; YouTube „Bravvo Band“ → „Peter Bravvo“ | Piotras | nepadaryta |
| 5 | Piotro prieiga: GitHub collaborator (bravvoband@gmail.com), Claude Pro, Hostinger GIT auto-deploy (šaka hostinger) | savininkas + Piotras | nepadaryta |
| 6 | Wikidata įrašas (juodraštis paleidimo pakete) | agentas, kai bus tinklo prieiga | nepadaryta |
| 7 | Katalogai, kuriuos AI cituoja: paslaugos.lt, breezit.lt | Piotras | nepadaryta |
| 8 | Patvirtinimai: Nickelodeon tekstu (dabar minimas tik kaip kanalas), gimimo metai NErašomi | Piotras | Nickelodeon neatsakyta |
| 9 | og:image (soc. tinklų peržiūros paveikslėlis) – kai bus portretinė nuotrauka | agentas | laukia #1 |

## Svarbu
- Svetainės kopija tik GitHub ir Hostinger. Po bet kokio pakeitimo: `./build.sh` → push → (kol nėra Hostinger GIT) zip į public_html.
- Faktai – tik iš Piotro atsakymų (Sheet 1-xHFk-XtyFqZKGwJb5NJoglS6xsIzn0vPEX-JkbGUNA). Sleeping Expert projekte neminimas.
