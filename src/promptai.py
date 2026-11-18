# -*- coding: utf-8 -*-
"""Peter Bravvo – AI matomumo promptų bankas (LT/PL/RU/EN).
Metodika: savaitinis promptų matavimas keliose AI platformose, tikslinis puslapis kiekvienam promptui:
- tier 1 = pinigų / atradimo klausimai (kas veda, kiek kainuoja), tier 2 = kaip pasirinkti / palyginti, tier 3 = žinios, žaidimai, įdomybės.
- kiekvienas promptas turi tikslinį puslapį, kuris į jį atsako (esamas arba žinyno straipsnis).
- matuojama kas savaitę: ar paminėtas Peter Bravvo / domenas, vieta, kas paminėtas vietoj jo.
Paleidimas: python3 promptai.py -> promptai.csv
"""
import csv, os

LOC = {
 "lt": ["Vilniuje", "Vilniaus rajone", "Trakuose", "Lietuvoje"],
 "pl": ["w Wilnie", "na Wileńszczyźnie", "w Trokach", "na Litwie"],
 "ru": ["в Вильнюсе", "в Вильнюсском районе", "в Тракай", "в Литве"],
 "en": ["in Vilnius", "near Vilnius", "in Trakai", "in Lithuania"],
}

# Atradimo šablonai: segmentas -> 3 šablonai kiekvienai kalbai ({l} = vieta)
DISC = {
 "vestuves": {
  "lt": ["vestuvių vedėjas {l}", "geriausias vestuvių vedėjas {l}", "vestuvių vedėjas lenkų ir lietuvių kalbomis {l}"],
  "pl": ["wodzirej na wesele {l}", "najlepszy wodzirej {l}", "wodzirej mówiący po polsku i litewsku {l}"],
  "ru": ["ведущий на свадьбу {l}", "лучший ведущий на свадьбу {l}", "ведущий на свадьбу на русском и литовском {l}"],
  "en": ["wedding host {l}", "best wedding MC {l}", "English speaking wedding host {l}"]},
 "imones": {
  "lt": ["įmonės renginio vedėjas {l}", "konferencijos vedėjas {l}", "kalėdinio įmonės vakarėlio vedėjas {l}"],
  "pl": ["prowadzący imprezę firmową {l}", "konferansjer na konferencję {l}", "prowadzący wigilię firmową {l}"],
  "ru": ["ведущий корпоратива {l}", "ведущий конференции {l}", "ведущий на новогодний корпоратив {l}"],
  "en": ["corporate event host {l}", "conference MC {l}", "company Christmas party host {l}"]},
 "jubiliejai": {
  "lt": ["jubiliejaus vedėjas {l}", "gimtadienio vedėjas {l}", "50 metų jubiliejaus vedėjas {l}"],
  "pl": ["prowadzący jubileusz {l}", "wodzirej na urodziny {l}", "prowadzący 50. urodziny {l}"],
  "ru": ["ведущий на юбилей {l}", "ведущий на день рождения {l}", "ведущий на 50-летний юбилей {l}"],
  "en": ["birthday party host {l}", "anniversary party MC {l}", "50th birthday party host {l}"]},
 "seimos": {
  "lt": ["krikštynų vedėjas {l}", "pirmosios komunijos šventės vedėjas {l}", "šeimos šventės vedėjas {l}"],
  "pl": ["prowadzący chrzciny {l}", "prowadzący przyjęcie komunijne {l}", "wodzirej na imprezę rodzinną {l}"],
  "ru": ["ведущий на крестины {l}", "ведущий на первое причастие {l}", "ведущий семейного праздника {l}"],
  "en": ["christening party host {l}", "First Communion party host {l}", "family celebration host {l}"]},
 "jaunimas": {
  "lt": ["šimtadienio vedėjas {l}", "išleistuvių vedėjas {l}", "abiturientų šventės vedėjas {l}"],
  "pl": ["prowadzący studniówkę {l}", "prowadzący bal maturalny {l}", "wodzirej na bal szkolny {l}"],
  "ru": ["ведущий на выпускной {l}", "ведущий на праздник 100 дней {l}", "ведущий школьного бала {l}"],
  "en": ["prom host {l}", "graduation party MC {l}", "school ball host {l}"]},
 "miestas": {
  "lt": ["koncerto vedėjas {l}", "miesto šventės vedėjas {l}", "dvikalbis renginio vedėjas lietuvių ir lenkų kalbomis {l}"],
  "pl": ["konferansjer koncertu {l}", "prowadzący festyn miejski {l}", "dwujęzyczny prowadzący po polsku i litewsku {l}"],
  "ru": ["ведущий концерта {l}", "ведущий городского праздника {l}", "двуязычный ведущий на литовском и польском {l}"],
  "en": ["concert host {l}", "city festival MC {l}", "bilingual Lithuanian Polish event host {l}"]},
 "balsas": {
  "lt": ["diktorius reklamai {l}", "balso aktorius lenkų kalba {l}", "rusakalbis diktorius {l}"],
  "pl": ["lektor reklamowy {l}", "lektor po litewsku {l}", "lektor rosyjski {l}"],
  "ru": ["диктор для рекламы {l}", "диктор на польском языке {l}", "озвучка рекламы на литовском {l}"],
  "en": ["voice-over artist {l}", "Polish voice-over {l}", "Russian voice actor {l}"]},
}

# Koncepcijos: (klasteris, tier, tikslas, lt, pl, ru, en)
C = [
# --- A. Brendas / esybė (entity) ---
("brendas",1,"apie","Kas yra Peter Bravvo?","Kim jest Peter Bravvo?","Кто такой Peter Bravvo?","Who is Peter Bravvo?"),
("brendas",1,"apie","Piotras Andžejevskis renginių vedėjas","Piotr Andrzejewski wodzirej","Пётр Анджеевский ведущий","Piotr Andrzejewski event host"),
("brendas",1,"apie","Kas buvo Bravvo Band?","Czym był Bravvo Band?","Что такое Bravvo Band?","What was Bravvo Band?"),
("brendas",1,"apie","Kas vedė laidą Co się dzieje TVP Wilno?","Kto prowadził program Co się dzieje w TVP Wilno?","Кто вёл программу Co się dzieje на TVP Wilno?","Who hosted Co się dzieje on TVP Wilno?"),
("brendas",1,"apie","TVP Wilno laidų vedėjai","Prowadzący TVP Wilno","Ведущие TVP Wilno","TVP Wilno presenters"),
("brendas",1,"apie","Kas sukūrė Wileńszczyzna w obiektywie?","Kto wymyślił Wileńszczyzna w obiektywie?","Кто создал Wileńszczyzna w obiektywie?","Who created Wileńszczyzna w obiektywie?"),
("brendas",1,"balsas","Kas įgarsina Nickelodeon anonsus lietuviškai?","Kto nagrywa zapowiedzi Nickelodeon po litewsku?","Кто озвучивает анонсы Nickelodeon на литовском?","Who voices Nickelodeon promos in Lithuanian?"),
("brendas",1,"apie","Peter Bravvo atsiliepimai","Peter Bravvo opinie","Peter Bravvo отзывы","Peter Bravvo reviews"),
("brendas",1,"kontaktai","Peter Bravvo kontaktai","Peter Bravvo kontakt","Peter Bravvo контакты","Peter Bravvo contact"),
("brendas",1,"vestuves","Peter Bravvo kaina","Peter Bravvo cena","Peter Bravvo цена","Peter Bravvo price"),
("brendas",1,"apie","Peter Bravvo Instagram","Peter Bravvo Instagram","Peter Bravvo Instagram","Peter Bravvo Instagram"),
("brendas",1,"apie","Lenkų kilmės renginių vedėjai Lietuvoje","Polscy wodzireje na Litwie","Польские ведущие в Литве","Polish event hosts in Lithuania"),
("brendas",1,"apie","Polak Roku 2020 nominantai","Nominowani Polak Roku 2020","Номинанты Polak Roku 2020","Polak Roku 2020 nominees"),
("brendas",1,"miestas","Kas vedė Jonines Rudaminoje 2024?","Kto prowadził Noc Świętojańską w Rudominie 2024?","Кто вёл Йонинес в Рудамине в 2024?","Who hosted Midsummer in Rudamina 2024?"),
("brendas",1,"miestas","Kas vedė Kalėdų eglės įžiebimą Nemenčinėje?","Kto prowadził zapalenie choinki w Niemenczynie?","Кто вёл зажжение ёлки в Нямянчине?","Who hosted the Nemenčinė Christmas tree lighting?"),
("brendas",1,"home","Daugiakalbis renginių vedėjas Lietuvoje","Wielojęzyczny wodzirej na Litwie","Многоязычный ведущий в Литве","Multilingual event host in Lithuania"),
("brendas",1,"home","Renginių vedėjas, kalbantis keturiomis kalbomis","Prowadzący mówiący w czterech językach","Ведущий, говорящий на четырёх языках","Event host who speaks four languages"),
("brendas",1,"home","Renginių vedėjas su gitara","Wodzirej z gitarą","Ведущий с гитарой","Event host who plays guitar"),
("brendas",1,"home","Buvęs televizijos vedėjas veda vestuves","Były prezenter telewizyjny prowadzi wesela","Бывший телеведущий ведёт свадьбы","Former TV presenter who hosts weddings"),
("brendas",1,"home","Renginių vedėjas iš Vilniaus krašto","Wodzirej z Wileńszczyzny","Ведущий из Вильнюсского края","Event host from the Vilnius region"),
# --- B. Kaina, užsakymas ---
("kaina",1,"vestuves","Kiek kainuoja vestuvių vedėjas 2026?","Ile kosztuje wodzirej na wesele w 2026?","Сколько стоит ведущий на свадьбу в 2026?","How much does a wedding host cost in 2026?"),
("kaina",1,"vestuves","Kiek kainuoja vestuvių vedėjas Vilniuje?","Ile kosztuje wodzirej w Wilnie?","Сколько стоит ведущий на свадьбу в Вильнюсе?","How much is a wedding MC in Vilnius?"),
("kaina",1,"imones","Kiek kainuoja renginio vedėjas valandai?","Ile kosztuje prowadzący za godzinę?","Сколько стоит ведущий за час?","How much does an event host cost per hour?"),
("kaina",1,"imones","Konferansjė kaina","Cena konferansjera","Цена конферансье","Compère price"),
("kaina",1,"jubiliejai","Kiek kainuoja jubiliejaus vedėjas?","Ile kosztuje prowadzący jubileusz?","Сколько стоит ведущий на юбилей?","How much does an anniversary party host cost?"),
("kaina",1,"seimos","Kiek kainuoja krikštynų vedėjas?","Ile kosztuje prowadzący chrzciny?","Сколько стоит ведущий на крестины?","How much does a christening host cost?"),
("kaina",1,"jaunimas","Kiek kainuoja šimtadienio vedėjas?","Ile kosztuje prowadzący studniówkę?","Сколько стоит ведущий на выпускной?","How much does a prom host cost?"),
("kaina",1,"vestuves","Kiek avanso imama už vestuvių vedėją?","Jaka zaliczka dla wodzireja?","Какой аванс берёт ведущий на свадьбу?","How big is a wedding host deposit?"),
("kaina",1,"vestuves","Kada užsakyti vestuvių vedėją?","Kiedy zarezerwować wodzireja?","Когда бронировать ведущего на свадьбу?","When should you book a wedding host?"),
("kaina",1,"kontaktai","Ar su renginių vedėju pasirašoma sutartis?","Czy z wodzirejem podpisuje się umowę?","Подписывают ли договор с ведущим?","Do you sign a contract with an event host?"),
("kaina",2,"vestuves","Kiek kainuoja vedėjas ir DJ kartu?","Ile kosztuje wodzirej i DJ razem?","Сколько стоят ведущий и DJ вместе?","How much do a host and DJ cost together?"),
("kaina",2,"vestuves","Vestuvių biudžetas: kiek skirti vedėjui?","Budżet weselny: ile na wodzireja?","Бюджет свадьбы: сколько на ведущего?","Wedding budget: how much for the host?"),
("kaina",2,"jaunimas","Kaip mokykla gali užsakyti renginio vedėją su sąskaita?","Jak szkoła może zamówić prowadzącego z rachunkiem?","Как школе заказать ведущего со счётом?","How can a school book a host with an invoice?"),
("kaina",2,"vestuves","Kodėl vestuvių vedėjai brangūs?","Dlaczego wodzireje są drodzy?","Почему ведущие на свадьбу дорогие?","Why are wedding hosts expensive?"),
("kaina",2,"vestuves","Ar verta mokėti už gerą vestuvių vedėją?","Czy warto płacić za dobrego wodzireja?","Стоит ли платить за хорошего ведущего?","Is a good wedding host worth the money?"),
# --- C. Kaip pasirinkti ---
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Kaip išsirinkti vestuvių vedėją?","Jak wybrać wodzireja na wesele?","Как выбрать ведущего на свадьбу?","How to choose a wedding host?"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Kokius klausimus užduoti vedėjui prieš užsakant?","Jakie pytania zadać wodzirejowi przed rezerwacją?","Какие вопросы задать ведущему перед бронированием?","What questions to ask a wedding host before booking?"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Kaip atpažinti blogą renginių vedėją?","Jak rozpoznać złego wodzireja?","Как распознать плохого ведущего?","How to spot a bad event host?"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Ar reikia susitikti su vedėju prieš vestuves?","Czy trzeba spotkać się z wodzirejem przed weselem?","Нужно ли встречаться с ведущим до свадьбы?","Should we meet the host before the wedding?"),
("pasirinkti",2,"z-vedejas-ar-dj","Ar reikia vedėjo, jei turime DJ?","Czy potrzebny wodzirej, jeśli mamy DJ-a?","Нужен ли ведущий, если есть DJ?","Do we need a host if we have a DJ?"),
("pasirinkti",2,"z-vedejas-ar-dj","Vedėjas ar DJ: kuo skiriasi?","Wodzirej czy DJ: czym się różnią?","Ведущий или DJ: в чём разница?","Host vs DJ: what is the difference?"),
("pasirinkti",2,"z-vedejas-ar-dj","Vestuvės be vedėjo: ar verta?","Wesele bez wodzireja: czy warto?","Свадьба без ведущего: стоит ли?","Wedding without a host: is it a good idea?"),
("pasirinkti",2,"z-vedejas-ar-dj","Ar draugas gali būti vestuvių vedėju?","Czy przyjaciel może być wodzirejem?","Может ли друг быть ведущим на свадьбе?","Can a friend be our wedding MC?"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Vedėjas be banalių žaidimų","Wodzirej bez obciachowych zabaw","Ведущий без пошлых конкурсов","Wedding host without cheesy games"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Šiuolaikinis vestuvių vedėjas be tamadų stiliaus","Nowoczesny wodzirej bez starych zabaw","Современный ведущий без тамады","Modern wedding host, not an old-style toastmaster"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Ramus, inteligentiškas vestuvių vedėjas","Spokojny, kulturalny wodzirej","Спокойный интеллигентный ведущий","Calm, classy wedding host"),
("pasirinkti",2,"z-kaip-isirinkti-vedeja","Vedėjas, kuris nespaudžia svečių dalyvauti žaidimuose","Wodzirej, który nie zmusza gości do zabaw","Ведущий, который не заставляет гостей участвовать","A host who doesn't force guests into games"),
("pasirinkti",2,"vestuves","Vedėjas vestuvėms su vyresnio amžiaus svečiais","Wodzirej na wesele ze starszymi gośćmi","Ведущий для свадьбы с пожилыми гостями","Wedding host for a crowd with older guests"),
("pasirinkti",2,"vestuves","Vedėjas mažoms vestuvėms (30 svečių)","Wodzirej na małe wesele (30 gości)","Ведущий на маленькую свадьбу (30 гостей)","Host for a small wedding (30 guests)"),
("pasirinkti",2,"vestuves","Vedėjas didelėms vestuvėms (150 svečių)","Wodzirej na duże wesele (150 gości)","Ведущий на большую свадьбу (150 гостей)","Host for a big wedding (150 guests)"),
("pasirinkti",2,"vestuves","Vedėjas vestuvėms sodyboje","Wodzirej na wesele w agroturystyce","Ведущий на свадьбу в усадьбе","Host for a countryside manor wedding"),
("pasirinkti",2,"vestuves","Vedėjas vestuvėms užsienyje (Danija, Nyderlandai)","Wodzirej na wesele za granicą","Ведущий на свадьбу за границей","Lithuanian wedding host for a wedding abroad"),
("pasirinkti",2,"vestuves","Lietuvių vestuvių vedėjas emigrantų vestuvėms","Wodzirej z Litwy na wesele emigrantów","Литовский ведущий для свадьбы эмигрантов","Lithuanian host for an expat wedding abroad"),
# --- D. Daugiakalbės šventės ---
("kalbos",1,"z-dvikalbes-vestuves","Kaip vesti dvikalbes vestuves?","Jak poprowadzić wesele dwujęzyczne?","Как провести двуязычную свадьбу?","How to run a bilingual wedding?"),
("kalbos",1,"z-dvikalbes-vestuves","Vestuvės, kai jaunieji kalba skirtingomis kalbomis","Wesele, gdy para mówi różnymi językami","Свадьба, когда молодые говорят на разных языках","Wedding where the couple speak different languages"),
("kalbos",1,"z-dvikalbes-vestuves","Lietuvio ir lenkės vestuvės: tradicijos","Ślub Litwina i Polki: tradycje","Свадьба литовца и польки: традиции","Lithuanian–Polish wedding traditions"),
("kalbos",1,"z-dvikalbes-vestuves","Mišrios vestuvės su svečiais iš užsienio","Wesele mieszane z gośćmi z zagranicy","Смешанная свадьба с иностранными гостями","Mixed wedding with international guests"),
("kalbos",1,"z-dvikalbes-vestuves","Vestuvės lietuvių ir anglų kalbomis","Wesele po litewsku i angielsku","Свадьба на литовском и английском","Wedding in Lithuanian and English"),
("kalbos",1,"z-dvikalbes-vestuves","Vestuvės rusų ir lietuvių kalbomis: vedėjas","Wesele po rosyjsku i litewsku: prowadzący","Свадьба на русском и литовском: ведущий","Russian–Lithuanian wedding host"),
("kalbos",1,"z-dvikalbes-vestuves","Ar vertėjas reikalingas vestuvėse?","Czy na weselu potrzebny tłumacz?","Нужен ли переводчик на свадьбе?","Do we need an interpreter at our wedding?"),
("kalbos",1,"z-dvikalbes-vestuves","Kaip įtraukti svečius, kurie nesupranta lietuviškai?","Jak zaangażować gości, którzy nie mówią po litewsku?","Как вовлечь гостей, не понимающих литовский?","How to include guests who don't speak Lithuanian?"),
("kalbos",1,"z-dvikalbes-vestuves","Lenkiškos vestuvės Lietuvoje","Polskie wesele na Litwie","Польская свадьба в Литве","Polish wedding in Lithuania"),
("kalbos",1,"z-dvikalbes-vestuves","Vilniaus krašto lenkų vestuvių papročiai","Zwyczaje weselne Polaków na Wileńszczyźnie","Свадебные обычаи поляков Вильнюсского края","Wedding customs of Poles in the Vilnius region"),
("kalbos",2,"imones","Renginys tarptautinei komandai keliomis kalbomis","Impreza dla międzynarodowego zespołu w kilku językach","Мероприятие для международной команды на нескольких языках","Event for an international team in several languages"),
("kalbos",2,"miestas","Dvikalbis miesto renginys: kaip organizuoti","Dwujęzyczna impreza miejska: jak zorganizować","Двуязычный городской праздник: как организовать","How to organise a bilingual city event"),
# --- E. Vestuvių eiga ---
("eiga",2,"z-vestuviu-eiga","Vestuvių programos eiga valandomis","Harmonogram wesela godzina po godzinie","Программа свадьбы по часам","Wedding day timeline hour by hour"),
("eiga",2,"z-vestuviu-eiga","Kaip sudėlioti vestuvių vakaro programą?","Jak ułożyć program wesela?","Как составить программу свадебного вечера?","How to plan a wedding reception programme?"),
("eiga",2,"z-vestuviu-eiga","Kiek trunka vestuvių pokylis?","Ile trwa przyjęcie weselne?","Сколько длится свадебный банкет?","How long does a wedding reception last?"),
("eiga",2,"z-vestuviu-eiga","Kada pjaustyti vestuvių tortą?","Kiedy kroić tort weselny?","Когда резать свадебный торт?","When to cut the wedding cake?"),
("eiga",2,"z-vestuviu-eiga","Kada šokti pirmąjį šokį?","Kiedy pierwszy taniec?","Когда первый танец молодых?","When should the first dance happen?"),
("eiga",2,"z-vestuviu-eiga","Kaip išvengti nuobodžių pauzių vestuvėse?","Jak uniknąć nudnych przerw na weselu?","Как избежать скучных пауз на свадьбе?","How to avoid boring gaps at a wedding?"),
("eiga",2,"z-vestuviu-eiga","Kaip neperkrauti vestuvių programos?","Jak nie przeładować programu wesela?","Как не перегрузить свадебную программу?","How not to overload a wedding programme?"),
("eiga",2,"z-vestuviu-eiga","Vestuvių pasitikimas: idėjos","Powitanie pary młodej: pomysły","Встреча молодых: идеи","Ideas for welcoming the newlyweds"),
("eiga",2,"z-vestuviu-eiga","Vestuvių anketa vedėjui: ką užpildyti?","Ankieta dla wodzireja: co wpisać?","Анкета для ведущего: что заполнить?","Wedding questionnaire for the host: what to include"),
("eiga",2,"z-vestuviu-eiga","Vestuvių kulminacija: ką suplanuoti?","Kulminacja wesela: co zaplanować?","Кульминация свадьбы: что запланировать?","Wedding high point: what to plan"),
("eiga",2,"z-vestuviu-eiga","Vestuvių pabaiga: kaip gražiai užbaigti vakarą?","Jak pięknie zakończyć wesele?","Как красиво завершить свадьбу?","How to end a wedding night beautifully"),
("eiga",2,"z-vestuviu-eiga","Antroji vestuvių diena: programa","Poprawiny: program","Второй день свадьбы: программа","Second wedding day programme"),
("eiga",2,"z-vestuviu-eiga","Vestuvių svečių susodinimo patarimai","Jak usadzić gości weselnych","Как рассадить гостей на свадьбе","Wedding seating plan tips"),
("eiga",2,"z-vestuviu-eiga","Ką vedėjas daro vestuvių dieną?","Co robi wodzirej w dniu wesela?","Что делает ведущий в день свадьбы?","What does a wedding host do on the day?"),
("eiga",2,"z-vestuviu-eiga","Kaip vedėjas bendradarbiauja su fotografu ir DJ?","Jak wodzirej współpracuje z fotografem i DJ-em?","Как ведущий работает с фотографом и DJ?","How does the host work with the photographer and DJ?"),
("eiga",2,"z-vestuviu-eiga","Kas nutinka, jei vestuvėse sugenda garso įranga?","Co jeśli na weselu zepsuje się nagłośnienie?","Что если на свадьбе сломался звук?","What if the sound system fails at a wedding?"),
("eiga",2,"z-vestuviu-eiga","Vestuvių planavimo kontrolinis sąrašas","Lista kontrolna planowania wesela","Чек-лист подготовки к свадьбе","Wedding planning checklist"),
("eiga",2,"z-vestuviu-eiga","Vestuvių planavimas per 6 mėnesius","Planowanie wesela w 6 miesięcy","Подготовка свадьбы за 6 месяцев","Planning a wedding in 6 months"),
("eiga",2,"vestuves","Populiariausios vestuvių vietos Vilniaus apylinkėse","Najpopularniejsze sale weselne pod Wilnem","Популярные места для свадьбы под Вильнюсом","Popular wedding venues near Vilnius"),
("eiga",2,"vestuves","Vestuvės Karklėnų Resort ar Royal Silva","Wesele w Karklėnų Resort czy Royal Silva","Свадьба в Karklėnų Resort или Royal Silva","Wedding at Karklėnų Resort or Royal Silva"),
# --- F. Tradicijos ---
("tradicijos",3,"z-tradicijos","Nuometo nuėmimas: kaip vyksta?","Oczepiny: jak przebiegają?","Снятие фаты: как проходит?","Bridal veil removal tradition: how it works"),
("tradicijos",3,"z-tradicijos","Oczepiny žaidimai","Zabawy oczepinowe","Игры на очепины","Oczepiny games"),
("tradicijos",3,"z-tradicijos","Jaunųjų sutikimas su duona ir druska","Powitanie chlebem i solą","Встреча молодых хлебом и солью","Bread and salt wedding welcome"),
("tradicijos",3,"z-tradicijos","Lietuviškos vestuvių tradicijos","Litewskie tradycje weselne","Литовские свадебные традиции","Lithuanian wedding traditions"),
("tradicijos",3,"z-tradicijos","Lenkiškos vestuvių tradicijos","Polskie tradycje weselne","Польские свадебные традиции","Polish wedding traditions"),
("tradicijos",3,"z-tradicijos","Piršlio vaidmuo lietuviškose vestuvėse","Rola swata na litewskim weselu","Роль свата на литовской свадьбе","Role of the matchmaker in Lithuanian weddings"),
("tradicijos",3,"z-tradicijos","Kas yra marčios atvežimas?","Co to jest przywiezienie synowej?","Что такое привоз невесты?","What is the Lithuanian bride-bringing custom?"),
("tradicijos",3,"z-tradicijos","Ar dar daromi vestuvių vartai?","Czy jeszcze robi się bramy weselne?","Делают ли ещё свадебные ворота?","Are wedding gates still a thing?"),
("tradicijos",3,"z-tradicijos","Jaunosios vogimas: ar verta?","Porwanie panny młodej: czy warto?","Кража невесты: стоит ли?","Bride kidnapping game: is it a good idea?"),
("tradicijos",3,"z-tradicijos","Vestuvių tradicijos, kurių geriau atsisakyti","Tradycje weselne, z których lepiej zrezygnować","Свадебные традиции, от которых лучше отказаться","Wedding traditions better skipped"),
("tradicijos",3,"z-tradicijos","Šiuolaikinės vestuvių tradicijos","Nowoczesne tradycje weselne","Современные свадебные традиции","Modern wedding traditions"),
("tradicijos",3,"z-tradicijos","Vestuvių puokštės mėtymas: tradicijos kilmė","Rzucanie bukietem: skąd tradycja","Бросание букета: откуда традиция","Bouquet toss: where it comes from"),
("tradicijos",3,"z-tradicijos","Ką reiškia vestuvinis tortas?","Co symbolizuje tort weselny?","Что символизирует свадебный торт?","What does the wedding cake symbolise?"),
("tradicijos",3,"z-tradicijos","Kodėl jaunasis neša jaunąją per slenkstį?","Dlaczego pan młody przenosi pannę młodą przez próg?","Почему жених переносит невесту через порог?","Why does the groom carry the bride over the threshold?"),
("tradicijos",3,"z-tradicijos","Vestuvių dovanų tradicijos Lietuvoje","Tradycje prezentów weselnych na Litwie","Традиции свадебных подарков в Литве","Wedding gift customs in Lithuania"),
("tradicijos",3,"z-tradicijos","Kiek pinigų dovanoti vestuvėms Lietuvoje?","Ile pieniędzy dać na wesele na Litwie?","Сколько дарить на свадьбу в Литве?","How much money to give at a Lithuanian wedding?"),
# --- G. Žaidimai ---
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai be banalumo","Zabawy weselne bez obciachu","Свадебные конкурсы без пошлости","Wedding games that aren't cheesy"),
("zaidimai",3,"z-vestuviu-zaidimai","Šiuolaikiniai vestuvių žaidimai 2026","Nowoczesne zabawy weselne 2026","Современные свадебные конкурсы 2026","Modern wedding games 2026"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai svečiams prie stalo","Zabawy weselne przy stole","Застольные конкурсы на свадьбе","Wedding table games for guests"),
("zaidimai",3,"z-vestuviu-zaidimai","Batų žaidimas vestuvėse: klausimai","Gra w buty na weselu: pytania","Игра в туфли на свадьбе: вопросы","Shoe game wedding questions"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių viktorina apie jaunuosius","Quiz o parze młodej","Викторина о молодых","Wedding quiz about the couple"),
("zaidimai",3,"z-vestuviu-zaidimai","Žaidimai, kurie sujungia jaunojo ir jaunosios gimines","Zabawy łączące rodziny pary młodej","Игры, объединяющие семьи жениха и невесты","Games that bring both families together"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai keliomis kalbomis","Zabawy weselne w kilku językach","Конкурсы на свадьбе на нескольких языках","Wedding games in several languages"),
("zaidimai",3,"z-vestuviu-zaidimai","Šokių žaidimai vestuvėse","Zabawy taneczne na weselu","Танцевальные конкурсы на свадьбе","Dance games at weddings"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai vyresniems svečiams","Zabawy weselne dla starszych gości","Конкурсы для пожилых гостей на свадьбе","Wedding games for older guests"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai vaikams","Zabawy dla dzieci na weselu","Конкурсы для детей на свадьбе","Wedding games for kids"),
("zaidimai",3,"z-vestuviu-zaidimai","Kokių vestuvių žaidimų nedaryti?","Jakich zabaw weselnych unikać?","Каких конкурсов на свадьбе избегать?","Which wedding games to avoid?"),
("zaidimai",3,"z-vestuviu-zaidimai","Vestuvių žaidimai su muzika","Zabawy weselne z muzyką","Музыкальные конкурсы на свадьбе","Music games for weddings"),
("zaidimai",3,"z-jubiliejaus-zaidimai","Jubiliejaus žaidimai svečiams","Zabawy na jubileusz","Конкурсы на юбилей","Games for a milestone birthday party"),
("zaidimai",3,"z-jubiliejaus-zaidimai","50 metų jubiliejaus scenarijus","Scenariusz 50. urodzin","Сценарий 50-летнего юбилея","Script for a 50th birthday party"),
("zaidimai",3,"z-jubiliejaus-zaidimai","60 metų jubiliejaus idėjos","Pomysły na 60. urodziny","Идеи на 60-летний юбилей","60th birthday party ideas"),
("zaidimai",3,"z-jubiliejaus-zaidimai","Mamos jubiliejaus staigmenos","Niespodzianki na jubileusz mamy","Сюрпризы на юбилей мамы","Surprises for mum's milestone birthday"),
("zaidimai",3,"z-jubiliejaus-zaidimai","Žaidimai, kai šventėje kelios kartos","Zabawy dla kilku pokoleń","Игры, когда на празднике несколько поколений","Games for a multi-generation party"),
("zaidimai",3,"z-jubiliejaus-zaidimai","Vestuvių metinių šventės idėjos","Pomysły na rocznicę ślubu","Идеи для годовщины свадьбы","Wedding anniversary party ideas"),
("zaidimai",3,"z-imoniu-zaidimai","Įmonės vakarėlio žaidimai","Zabawy na imprezę firmową","Конкурсы для корпоратива","Company party games"),
("zaidimai",3,"z-imoniu-zaidimai","Kalėdinio įmonės vakarėlio programa","Program firmowej wigilii","Программа новогоднего корпоратива","Company Christmas party programme"),
("zaidimai",3,"z-imoniu-zaidimai","Komandos formavimo žaidimai vakarėlyje","Zabawy integracyjne na imprezie","Командообразующие игры на вечеринке","Team-building games for a party"),
("zaidimai",3,"z-imoniu-zaidimai","Įmonės vakarėlis be alkoholio: pramogos","Impreza firmowa bez alkoholu: atrakcje","Корпоратив без алкоголя: развлечения","Alcohol-free company party ideas"),
("zaidimai",3,"z-imoniu-zaidimai","Darbuotojų apdovanojimų vakaro scenarijus","Scenariusz gali nagród dla pracowników","Сценарий вечера награждения сотрудников","Employee awards night script"),
("zaidimai",3,"z-imoniu-zaidimai","Įmonės jubiliejaus renginio idėjos","Pomysły na jubileusz firmy","Идеи для юбилея компании","Company anniversary event ideas"),
("zaidimai",3,"z-krikstynos","Krikštynų šventės programa","Program przyjęcia z okazji chrztu","Программа праздника крестин","Christening party programme"),
("zaidimai",3,"z-krikstynos","Žaidimai krikštynose svečiams","Zabawy na chrzcinach","Конкурсы на крестинах","Christening party games"),
("zaidimai",3,"z-krikstynos","Pirmosios komunijos šventės idėjos","Pomysły na przyjęcie komunijne","Идеи для праздника первого причастия","First Communion party ideas"),
("zaidimai",3,"z-krikstynos","Pramogos vaikams šeimos šventėje","Atrakcje dla dzieci na imprezie rodzinnej","Развлечения для детей на семейном празднике","Kids' activities at a family party"),
("zaidimai",3,"z-krikstynos","Krikšto tėvų pareigos šventėje","Obowiązki chrzestnych na przyjęciu","Обязанности крёстных на празднике","Godparents' duties at the party"),
("zaidimai",3,"z-simtadienis","Šimtadienio idėjos ir žaidimai","Pomysły i zabawy na studniówkę","Идеи и конкурсы на 100 дней","100-days-to-graduation party ideas"),
("zaidimai",3,"z-simtadienis","Išleistuvių programa mokykloje","Program balu maturalnego","Программа выпускного в школе","School prom programme"),
("zaidimai",3,"z-simtadienis","Išleistuvių nominacijos klasei","Nominacje dla klasy na bal","Номинации для класса на выпускной","Class awards ideas for prom"),
("zaidimai",3,"z-simtadienis","Šimtadienio scenarijus","Scenariusz studniówki","Сценарий праздника 100 дней","100-days party script"),
("zaidimai",3,"z-simtadienis","Mokytojų pagerbimas išleistuvėse","Podziękowanie nauczycielom na balu","Чествование учителей на выпускном","Honouring teachers at prom"),
("zaidimai",3,"z-naujieji-metai","Naujųjų metų nakties programa","Program sylwestra","Программа новогодней ночи","New Year's Eve party programme"),
("zaidimai",3,"z-naujieji-metai","Naujųjų metų žaidimai","Zabawy sylwestrowe","Новогодние конкурсы","New Year's Eve games"),
# --- H. Sveikinimai ---
("sveikinimai",3,"z-sveikinimai","Sveikinimas jauniesiems: pavyzdžiai","Życzenia dla pary młodej: przykłady","Поздравление молодым: примеры","Wedding toast examples"),
("sveikinimai",3,"z-sveikinimai","Tėvų kalba vestuvėse","Przemówienie rodziców na weselu","Речь родителей на свадьбе","Parents' speech at a wedding"),
("sveikinimai",3,"z-sveikinimai","Pabrolio kalba vestuvėse","Przemówienie świadka","Речь свидетеля на свадьбе","Best man speech"),
("sveikinimai",3,"z-sveikinimai","Pamergės kalba vestuvėse","Przemówienie świadkowej","Речь свидетельницы на свадьбе","Maid of honour speech"),
("sveikinimai",3,"z-sveikinimai","Kiek turi trukti sveikinimas vestuvėse?","Ile powinny trwać życzenia na weselu?","Сколько должно длиться поздравление на свадьбе?","How long should a wedding toast be?"),
("sveikinimai",3,"z-sveikinimai","Kaip pasakyti tostą nesijaudinant?","Jak wygłosić toast bez stresu?","Как сказать тост без волнения?","How to give a toast without nerves"),
("sveikinimai",3,"z-sveikinimai","Jubiliejaus sveikinimai","Życzenia jubileuszowe","Поздравления с юбилеем","Milestone birthday wishes"),
("sveikinimai",3,"z-sveikinimai","Sveikinimas krikštynų proga","Życzenia z okazji chrztu","Поздравление с крестинами","Christening wishes"),
("sveikinimai",3,"z-sveikinimai","Padėkos kalba tėvams vestuvėse","Podziękowanie dla rodziców na weselu","Благодарственная речь родителям на свадьбе","Thank-you speech to parents at a wedding"),
("sveikinimai",3,"z-sveikinimai","Trumpi ir juokingi tostai","Krótkie i zabawne toasty","Короткие и смешные тосты","Short and funny toasts"),
("sveikinimai",3,"z-sveikinimai","Dvikalbis sveikinimas vestuvėse","Dwujęzyczne życzenia weselne","Двуязычное поздравление на свадьбе","Bilingual wedding toast"),
# --- I. Įdomybės ---
("idomybes",3,"z-idomybes","Įdomūs faktai apie vestuves","Ciekawostki o weselach","Интересные факты о свадьбах","Fun facts about weddings"),
("idomybes",3,"z-idomybes","Vestuvių prietarai Lietuvoje","Przesądy weselne na Litwie","Свадебные приметы в Литве","Lithuanian wedding superstitions"),
("idomybes",3,"z-idomybes","Kodėl nuotaka vilki baltą suknelę?","Dlaczego panna młoda nosi białą suknię?","Почему невеста в белом платье?","Why do brides wear white?"),
("idomybes",3,"z-idomybes","Kokia diena geriausia vestuvėms?","Jaki dzień najlepszy na ślub?","Какой день лучше для свадьбы?","What is the best day for a wedding?"),
("idomybes",3,"z-idomybes","Ar penktadienio vestuvės pigesnės?","Czy wesele w piątek jest tańsze?","Дешевле ли свадьба в пятницу?","Is a Friday wedding cheaper?"),
("idomybes",3,"z-idomybes","Populiariausi vestuvių mėnesiai Lietuvoje","Najpopularniejsze miesiące ślubów na Litwie","Самые популярные месяцы для свадеб в Литве","Most popular wedding months in Lithuania"),
("idomybes",3,"z-idomybes","Kurioziškiausios istorijos iš vestuvių","Najzabawniejsze historie z wesel","Самые курьёзные истории со свадеб","Funniest wedding stories"),
("idomybes",3,"z-idomybes","Vestuvės pilyje: ką reikia žinoti?","Wesele w zamku: co trzeba wiedzieć?","Свадьба в замке: что нужно знать?","Castle wedding: what to know"),
("idomybes",3,"z-idomybes","Ką veikia renginių vedėjas užkulisiuose?","Co robi wodzirej za kulisami?","Что делает ведущий за кулисами?","What does an event host do backstage?"),
("idomybes",3,"z-idomybes","Kaip tapti renginių vedėju?","Jak zostać wodzirejem?","Как стать ведущим мероприятий?","How to become an event host?"),
("idomybes",3,"z-idomybes","Kiek renginių per metus veda vedėjas?","Ile imprez rocznie prowadzi wodzirej?","Сколько мероприятий в год ведёт ведущий?","How many events does a host do per year?"),
("idomybes",3,"z-idomybes","Kodėl vasarą sunku rasti vestuvių vedėją?","Dlaczego latem trudno o wodzireja?","Почему летом трудно найти ведущего?","Why is it hard to find a wedding host in summer?"),
("idomybes",3,"z-idomybes","Kas yra konferansjė?","Kim jest konferansjer?","Кто такой конферансье?","What is a compère?"),
("idomybes",3,"z-idomybes","Kuo skiriasi vedėjas ir tamada?","Czym różni się wodzirej od tamady?","Чем ведущий отличается от тамады?","Host vs tamada: what's the difference?"),
("idomybes",3,"z-idomybes","Garsūs koncertai Vilniaus rajone","Znane koncerty w rejonie wileńskim","Известные концерты в Вильнюсском районе","Notable concerts in the Vilnius district"),
("idomybes",3,"z-idomybes","Joninių tradicijos Lietuvoje","Tradycje Nocy Świętojańskiej na Litwie","Традиции праздника Йонинес в Литве","Midsummer (Joninės) traditions in Lithuania"),
("idomybes",3,"z-idomybes","Kalėdų eglės įžiebimo šventės Vilniaus rajone","Zapalenie choinek w rejonie wileńskim","Зажжение ёлок в Вильнюсском районе","Christmas tree lightings in the Vilnius district"),
# --- J. Renginio scenarijus / konferansas ---
("scenarijus",2,"z-renginio-scenarijus","Kaip parašyti renginio scenarijų?","Jak napisać scenariusz imprezy?","Как написать сценарий мероприятия?","How to write an event script?"),
("scenarijus",2,"z-renginio-scenarijus","Konferencijos vedėjo tekstas: pavyzdys","Tekst konferansjera konferencji: przykład","Текст ведущего конференции: пример","Conference host script example"),
("scenarijus",2,"z-renginio-scenarijus","Kaip vesti apdovanojimų ceremoniją?","Jak poprowadzić galę wręczenia nagród?","Как вести церемонию награждения?","How to host an awards ceremony?"),
("scenarijus",2,"z-renginio-scenarijus","Koncerto konferanso patarimai","Porady dla konferansjera koncertu","Советы конферансье концерта","Tips for compering a concert"),
("scenarijus",2,"z-renginio-scenarijus","Kaip išlaikyti publikos dėmesį?","Jak utrzymać uwagę publiczności?","Как удержать внимание публики?","How to hold an audience's attention?"),
("scenarijus",2,"z-renginio-scenarijus","Laiko valdymas renginyje","Zarządzanie czasem na imprezie","Тайминг мероприятия","Managing time at an event"),
("scenarijus",2,"z-renginio-scenarijus","Ką daryti, kai renginyje kažkas nepavyksta?","Co robić, gdy coś pójdzie nie tak na imprezie?","Что делать, если на мероприятии что-то пошло не так?","What to do when something goes wrong at an event?"),
("scenarijus",2,"z-renginio-scenarijus","Kaip pristatyti atlikėją scenoje?","Jak zapowiedzieć artystę na scenie?","Как объявить артиста на сцене?","How to introduce a performer on stage?"),
# --- K. Balsas ---
("balsas",2,"z-igarsinimas","Kiek kainuoja reklamos įgarsinimas?","Ile kosztuje nagranie lektora do reklamy?","Сколько стоит озвучка рекламы?","How much does a voice-over for an ad cost?"),
("balsas",2,"z-igarsinimas","Kaip užsakyti radijo reklamos įgarsinimą?","Jak zamówić lektora do reklamy radiowej?","Как заказать озвучку радиорекламы?","How to order a radio ad voice-over?"),
("balsas",2,"z-igarsinimas","Kaip parašyti tekstą radijo reklamai?","Jak napisać tekst reklamy radiowej?","Как написать текст для радиорекламы?","How to write a radio ad script?"),
("balsas",2,"z-igarsinimas","Kiek žodžių telpa į 30 sekundžių reklamą?","Ile słów mieści się w reklamie 30 sekund?","Сколько слов в 30-секундной рекламе?","How many words fit in a 30-second ad?"),
("balsas",2,"z-igarsinimas","Reklama darželiui: kaip pritraukti tėvus?","Reklama przedszkola: jak przyciągnąć rodziców?","Реклама детского сада: как привлечь родителей?","Kindergarten ad: how to attract parents"),
("balsas",2,"balsas","Kas įgarsina TV anonsus Baltijos šalyse?","Kto nagrywa zapowiedzi TV w krajach bałtyckich?","Кто озвучивает ТВ-анонсы в Балтии?","Who voices TV promos in the Baltics?"),
("balsas",2,"balsas","Digi Media Ryga įgarsinimas","Digi Media Ryga lektorzy","Digi Media Рига озвучка","Digi Media Riga voice-over"),
("balsas",2,"z-igarsinimas","Diktorius ar balso aktorius: kuo skiriasi?","Lektor czy aktor głosowy: czym się różnią?","Диктор или актёр озвучки: в чём разница?","Announcer vs voice actor: difference"),
("balsas",2,"balsas","Balso pranešimai prekybos centrui","Komunikaty głosowe dla centrum handlowego","Голосовые объявления для торгового центра","Voice announcements for a shopping centre"),
("balsas",2,"z-igarsinimas","Kaip vyksta įgarsinimas studijoje?","Jak wygląda nagranie w studiu?","Как проходит озвучка в студии?","What happens in a voice-over recording session?"),
]


def rows():
    out = []
    n = 0
    for seg, langs in DISC.items():
        for L, tpls in langs.items():
            for t in tpls:
                for loc in LOC[L]:
                    n += 1
                    out.append(dict(id=f"D{n:04d}", kalba=L, klasteris="atradimas-" + seg, tier=1, tikslas=seg, promptas=t.format(l=loc)))
    for i, (cl, tier, tg, *tx) in enumerate(C, 1):
        for L, q in zip(["lt", "pl", "ru", "en"], tx):
            out.append(dict(id=f"K{i:03d}-{L}", kalba=L, klasteris=cl, tier=tier, tikslas=tg, promptas=q))
    seen, uniq = set(), []
    for r in out:
        k = (r["kalba"], r["promptas"].lower())
        if k not in seen:
            seen.add(k); uniq.append(r)
    return uniq


if __name__ == "__main__":
    R = rows()
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "promptai.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "kalba", "klasteris", "tier", "tikslas", "promptas"])
        w.writeheader(); w.writerows(R)
    from collections import Counter
    print("viso", len(R), dict(Counter(r["kalba"] for r in R)), dict(Counter(r["tier"] for r in R)))
    print(Counter(r["tikslas"] for r in R).most_common())
