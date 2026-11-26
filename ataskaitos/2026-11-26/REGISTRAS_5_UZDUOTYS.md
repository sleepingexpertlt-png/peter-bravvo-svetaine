# 5 задач реестра Bravo Band (26.11, вечер) — ветка `claude/bravo-registras-2026-11-26`, НЕ опубликовано
Все изменения сайта — только в ветке/PR. На живой peterbravvo.lt ничего не выложено (FTP-деплой запускается только из main).

## task-bravo-sameas-decision-001 — sameAs
Добавлено в Person.sameAs (все страницы): Instagram peter_bravvo, Instagram bravvoband, Facebook PeterBravvo, Facebook BravvoBAND, YouTube UCcw58zifBWeADgGHDDlQALg и @bravvoband5082. Mozello нет, двойники исключены.
Сверка: Instagram peter_bravvo — поле «сайт» в GBP; Facebook BravvoBAND и Instagram bravvoband — каталог Vestuves Plius с тем же тел. 37060703318 и bravvoband@gmail.com; YouTube — названия «Peter Bravvo | VEDĖJAS…» и ссылка на instagram peter_bravvo в описаниях; Facebook PeterBravvo — решение владельца (Facebook/Instagram без входа не открываются — живой страницей не сверено).

## task-bravo-made-by-marshalls-001 + task-bravo-powered-by-text-001 — подвал
Сверено с живым сайтом https://marsalas.lt (26.11): name «Maršalas», legalName «Maršalas, MB», @id https://marsalas.lt/#organization. **marshalls.lt не открывается (домен не отвечает)** — использован marsalas.lt.
Подвал всех 120 страниц (LT/PL/RU/EN одинаково, по-английски): «Powered by MB Maršalas» → https://marsalas.lt (обычная ссылка, rel=noopener).
JSON-LD WebSite: creator = Organization Maršalas (legalName «Maršalas, MB», url marsalas.lt), maintainer = он же; publisher остаётся Пётр. Авторство текстов Пётра не трогали.

## task-bravo-voiceover-service-001 — озвучка
Страница услуги уже есть (/diktorius/ и 3 языка) + статья «Reklamos įgarsinimas». Добавлено в схему страницы: serviceType [Balsas reklamai, Voice-over, Radio advertising voice, TV promo voice], availableLanguage = lt, pl, ru (как написано на странице по данным владельца).
**Студия: нет подтверждённых данных** (адрес, название, оборудование) → LocalBusiness студии НЕ добавлен. **Демо-записей нет** → AudioObject НЕ добавлен. В видео-архиве (180 роликов) отдельных образцов озвучки не найдено; в портрете TVP Пётр говорит, что его можно услышать «w radiu jako voiceover» (04:33).
Вопросы владельцу/Пётру: 1) есть ли своя студия — название, город (адрес публиковать?); 2) оборудование; 3) форматы (радио, ТВ, видео, IVR, аудиогиды); 4) цены и сроки; 5) 2–3 демо-файла (свои права, без логотипов каналов); 6) можно ли называть заказчиков (Digi Media, «Kaštonas», школа на Антакальнисе — уже на сайте по данным владельца).
Текст для GBP (на утверждение): услуга «Reklamos įgarsinimas / balso reklama» — «Įgarsinu reklamas radijui, TV ir internetui lietuvių, lenkų ir rusų kalbomis. Atsiųskite tekstą – pasiūlysiu tempą ir toną.» Категорию добавить: «Balso aktorius» (если есть в списке категорий GBP — проверить в кабинете).

## task-bravo-landing-pages-001 — посадочные страницы
**Главный итог:** 3 новые страницы-ответа × 4 языка = 12 страниц (сайт 108 → 120) по реальным подсказкам Google:
- «kiek kainuoja vestuvių vedėjas» / «ile kosztuje wodzirej na wesele» / «сколько стоит ведущий на свадьбу» / «how much does a wedding host cost» — подсказки «vestuvių vedėjas kaina», «wodzirej na wesele cena», «ведущий на свадьбу цена», «wedding mc price». Цены только из данных владельца (от 1000 €, 200 €/ч, аванс 300 €); цена DJ — «по дате и месту» (неизвестна).
- «vedėjas su DJ» / «wodzirej z DJ» / «ведущий с DJ» / «host with a DJ» — подсказки «vestuvių vedėjas su dj», «vedėjas dj». Основа — пост GBP 05.11 (своя команда: DJ, звук, свет).
- «Vilniaus rajonas» — только подтверждённые события: Joninės Rudamina 2024 (с DJ Jovani; rudaminoskultura.lt, vrtic.lt), ёлка Nemenčinė и Rudamina, Dožinkos Kabiškės (данные владельца).
Формат каждой: ответ в первых строках → что входит/подробности → «Tinka, jei / Netinka, jei» → FAQ (FAQPage) → связка с услугой; Article + author Person (как в базе знаний). Один URL — один контент для людей и роботов.
Не сделано (нет данных): страницы городов кроме Вильнюсского района (Каунас и др. — где работал, не подтверждено), Joninės отдельной страницей (одно событие), пакеты с ценами, отзывы. Рекламные посадочные — только план: «vestuvių vedėjas kaina» → страница цены; «vedėjas su DJ» → страница DJ; бюджет 0 до решения владельца.
Практики для сайтов ведущих (источники проверены поиском 26.11): каталоги с отзывами (paslaugos.lt — средние цены 200–800 € за ведение публичных мероприятий видны прямо в поиске), страницы «как выбрать ведущего» у каталогов (paslaugos.lt/renginiu-vedejai/kaip-issirinkti), видео-примеры ведения, отзывы с именами — подробно в AUDITAS.md и BACKLINKAI.md.
Search Console к сайту не подключён (нет токена верификации) — данных о запросах сайта нет.
