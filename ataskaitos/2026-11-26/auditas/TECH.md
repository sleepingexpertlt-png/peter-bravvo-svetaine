# Технический аудит peterbravvo.lt (live), 2026-11-26

Только чтение. Сырой вывод: `raw_http.txt`, `raw_crawl.txt`, `raw_html_checks.txt`, `raw_perf_console.txt`, `raw_external.txt` в этой же папке. Скриншоты: `shots/`.
Ограничение среды: прокси контейнера пропускает только `https://peterbravvo.lt` (apex). `http://` и `www.` с этого контейнера проверить НЕЛЬЗЯ (DNS не резолвится / CONNECT 403 от прокси) — это не результат сервера.

## Таблица проверок

| Проверка | Статус | Evidence |
|---|---|---|
| HTTP статус / | OK | `HTTP/2 200`, `server: hcdn` (Hostinger CDN) |
| TLS сертификат | OK | `CN=peterbravvo.lt`, issuer `Let's Encrypt CN=YE2`, start Nov 24 2026, expire **Feb 22 2027 GMT**, `SSL certificate verify ok` (curl -v) |
| http -> https | НЕ ПРОВЕРЕНО | прокси контейнера; в ответе есть `content-security-policy: upgrade-insecure-requests` |
| www -> apex | НЕ ПРОВЕРЕНО | `CONNECT tunnel failed, response 403` (прокси) |
| sitemap.xml | OK | 108 `<loc>`, все 108 = HTTP 200 (по 27 на LT/PL/RU/EN) |
| Битые внутренние ссылки/картинки | OK | со всех 108 страниц собрано 154 уникальных внутренних цели (`<a>`, `<img>`, source/link) — 0 не-200 |
| Внешние ссылки (39 уник.) | частично | 200: 17 (l24, vrsa, vrtic, kurierwilenski, tvp, facebook, share.google, youtube channel); 429 от youtube/instagram (антибот, не битые); 8 не проверены (прокси 403: wa.me, wilnoteka, delfi, lrt, madeinvilnius, vilnijosnaujienos) |
| hreflang | OK | все 108 страниц имеют hreflang (lt/pl/ru/en/x-default); проверены ВСЕ 540 пар: каждая альтернатива есть в sitemap, есть self-ref и обратная ссылка — 0 проблем. x-default = LT-версия |
| JSON-LD | OK | у всех 108 страниц есть, 0 ошибок парсинга. Типы (кол-во по сайту): Person 108, WebSite 108, ProfessionalService 108, TVSeries 108, OfferCatalog 108, VideoObject 224, FAQPage 96 (Question/Answer 742), Article 384, Event 48 (+Place/PostalAddress 48), BreadcrumbList 104, Service 248, Offer 244, ProfilePage/AboutPage/ContactPage/CollectionPage по 4 |
| robots.txt | OK | `User-agent: *` Allow /; явно Allow для GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Bingbot; `Sitemap: https://peterbravvo.lt/sitemap.xml`. (Нет отдельных блоков для Googlebot — покрыт `*`.) |
| llms.txt | OK | `/llms.txt` 200, `/llms-full.txt` 200 |
| 404 | OK | несуществующий URL -> `HTTP/2 404` (не soft-404); `/zinynas` -> 301 `/zinynas/` |
| Изображения | OK | 45 webp в ссылках; крупнейшие: p41 277 024 B, p42 130 738, p33 106 974, p19 100 776, p39 96 762, p43 70 580, p38 67 424, p52 65 208, p18 61 506, p54 60 832. Только webp; og:image — jpg (`/foto/og/home-lt.jpg`) |
| Вес / (iPhone 13, холодная загрузка) | OK | 11 запросов, 493 671 B (HTML 61 931, CSS Google Fonts 22 265, 7 woff2 = 296 304, hero webp 100 776, 1 jpeg 12 395 — YouTube thumb) |
| Тайминги / mobile (Playwright) | OK | TTFB 410 мс, FCP 640 мс, DCL 633 мс, load 993 мс (прогон 1, холодный); прогон 2 (кэш): DCL 116, load 132 |
| Console errors (6 страниц: /, /vestuviu-vedejas/, /pl/wodzirej-wesele/, /apie/, /zinynas/dvikalbes-vestuves-vedejas/, /kontaktai/) | OK | error/warning/pageerror/requestfailed: none на всех (после скролла вниз) |
| viewport meta | OK | на всех 108: `width=device-width,initial-scale=1`; `<html lang>` задан везде (lt/pl/ru/en по 27) |
| Дубли title | OK | 0 дублей среди 108 |
| Title > 60 (LT) | проблема | 7 из 27 LT (всего 19 из 108): `/` (83), `/pristatymu-konferenciju-vedejas/` (72), `/koncertu-svenciu-vedejas/` (61), `/zinynas/reklamos-igarsinimas-kaina-tekstas-studija/` (62), `/zinynas/imones-vakarelio-zaidimai-programa/` (61), `/zinynas/naujuju-metu-nakties-programa-zaidimai/` (65), `/zinynas/simtadienio-isleistuviu-programa-idejos/` (61). В PL/RU/EN ещё 12 (напр. `/pl/` 75, `/ru/` 81, `/en/` 80) |
| Description > 160 | OK | макс. 157 (`/en/wedding-host/`); у всех description есть, самый короткий 103 |
| canonical / h1 | OK | canonical и ровно один h1 на всех страницах (флагов нет) |
| Security-заголовки | проблема | в ответе нет `strict-transport-security`, `x-frame-options`, `referrer-policy`, `x-content-type-options` (есть только `content-security-policy: upgrade-insecure-requests`) |
| Кэш HTML | замечание | у HTML нет `cache-control` (есть `etag`, `last-modified`); у webp `max-age=604800` (7 дней) |
| Шрифты | замечание | 7 woff2 (296 KB, 60% веса страницы) + CSS грузятся с fonts.googleapis.com / fonts.gstatic.com (сторонний домен), не self-hosted |
| alt у изображений | замечание | на 108 страницах 468 `<img>`: 216 с alt, 252 с `alt=""`, без атрибута alt — 0. Пустой alt, напр., у hero `/foto/h/p19.webp` и у YouTube-превью (`i.ytimg.com`, `alt=""`) на `/` |

## Конкретные дефекты

1. Title слишком длинный (>60): `/` = 83 символа, `/pl/` 75, `/ru/` 81, `/en/` 80; `/pristatymu-konferenciju-vedejas/` 72; ещё 5 LT-страниц 61-65 (список в таблице). Источник: `src/turinys.py` / `src/build2.py`.
2. Нет HSTS / X-Frame-Options / Referrer-Policy / X-Content-Type-Options (заголовки отдаёт Hostinger; правятся в hPanel или `.htaccess`).
3. Шрифты Google Fonts — внешний домен, 296 KB woff2 (самый тяжёлый ресурс после hero: `Unbounded` 117 648 B + 50 892 B).
4. 252 `<img alt="">`, включая YouTube-превью видео на главной (контентные картинки без описания).
5. Мобильный первый экран `/`: воздушные шарики (анимация) частично перекрывают переключатель языков (буквы "RU" частично закрыты) — см. `shots/mobile_home_fold.png`.
6. Не проверено из-за прокси: редирект http->https, www->apex, 8 внешних ссылок (wa.me, wilnoteka x2, delfi, lrt, madeinvilnius, vilnijosnaujienos). Проверить с обычной сети: `curl -sIL http://peterbravvo.lt/ http://www.peterbravvo.lt/`.

Скриншоты (desktop 1366x900 и iPhone 13, dsf 1): `shots/{desktop,mobile}_{home,vestuviu,pl_wesele,imoniu,apie,kontaktai,zinynas}_fold.png`, плюс `shots/mobile_home_fullpage.png`, `shots/desktop_home_fullpage.png`. Страницы: `/`, `/vestuviu-vedejas/`, `/pl/wodzirej-wesele/`, `/imoniu-renginiu-vedejas/`, `/apie/`, `/kontaktai/`, `/zinynas/dvikalbes-vestuves-vedejas/`.
