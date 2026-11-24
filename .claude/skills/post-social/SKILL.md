---
name: post-social
description: Tworzy gotowy post na Instagram/Facebook (Reels lub karuzela) dla Petera Bravvo z pytania z banku AEO i artykułu z poradnika. Używaj, gdy Piotr mówi „zrób post”, „pomysł na rolkę”, „co wrzucić na Insta”, „opis do filmu”.
---

# Post na Instagram / Facebook

1. Wybierz pytanie: jeśli Piotr nie podał tematu, weź z `aeo/promptai.csv` pytanie z tier 2 lub 3 w języku, o który prosi (domyślnie PL), którego jeszcze nie było (sprawdź `soc/opublikowane.csv`, jeśli istnieje).
2. Znajdź odpowiedź w `src/zinynas/<temat>.json` (pole `faq` lub `sections`) albo w `src/turinys.py`. Używaj tylko faktów z CLAUDE.md.
3. Zwróć Piotrowi DOKŁADNIE ten format:

```
🎬 FORMAT: Reels 20–40 s (mówisz do kamery) | albo Karuzela 5–7 slajdów
🎤 CO POWIEDZIEĆ / SLAJDY:
1. [hak: pytanie, 1 zdanie]
2. [odpowiedź, 2–3 krótkie zdania]
3. [przykład z praktyki Piotra, jeśli pasuje]
4. [CTA: „Termin? Napisz na WhatsApp – link w bio”]
📝 OPIS:
[pytanie]
[2–3 zdania odpowiedzi]
Pełny poradnik → link w bio (peterbravvo.lt)
#wodzirej #wodzirejwilno #weseleNaLitwie #vestuviuvedejas #renginiuvedejas
🔗 LINK DO ARTYKUŁU: https://peterbravvo.lt/<ścieżka>
```

4. Dopisz wiersz do `soc/opublikowane.csv` (data, język, pytanie, link) i zrób commit.

Zasady: bez wymyślonych liczb, bez nazw firm-klientów, bez „najlepszy”. Krótko. Język zgodny z prośbą (PL / LT / RU).
