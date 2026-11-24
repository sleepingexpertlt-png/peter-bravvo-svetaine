---
name: raport-aeo
description: Raport widoczności Petera Bravvo w odpowiedziach AI na podstawie bota AEO. Używaj, gdy Piotr pyta „jak wypadamy w AI”, „czy ChatGPT mnie zna”, „raport”, „co poprawić w widoczności”.
---

# Raport AEO

1. `git pull` i przeczytaj `aeo/rezultatai/SUVESTINE.md` oraz najnowszy `aeo/rezultatai/*.csv`.
2. Podaj Piotrowi max 6 linijek:
   - ile pytań sprawdzono łącznie i w ostatnich 7 dniach,
   - % „wspomniany” i % „cytowany (peterbravvo.lt)” – ogółem i najlepszy/najgorszy język,
   - 3 domeny najczęściej cytowane zamiast niego (konkurencja / katalogi),
   - 1–2 konkretne działania: np. artykuł do poradnika na temat z najniższym wynikiem, profil w katalogu, który AI cytuje (paslaugos.lt, breezit.lt), prośba o opinie Google.
3. Pamiętaj: bot używa darmowego modelu bez wyszukiwania internetu – mierzy, co model „wie”. Wzrost przychodzi z czasem (strona, cytaty, opinie, Wikidata), nie z samego zadawania pytań.
4. Jeśli `SUVESTINE.md` nie istnieje albo bot nie działał: sprawdź zakładkę Actions → „AEO botas”. Najczęstsza przyczyna: brak sekretu `OPENROUTER_API_KEY` (GitHub → Settings → Secrets → Actions).
