"""Общий корпус для опытов с токенайзерами.

PARALLEL — одна и та же мысль на 7 языках/письменностях (сравнивается с английским).
NEUTRAL  — тексты, не привязанные к языку: числа, код, JSON, URL, эмодзи.

Переводы сделаны вручную и носителями не проверялись; смысл совпадает, формулировки
могут отличаться от «идеальных».
"""

LANGS = {
    "en": "English",
    "ru": "Русский",
    "ru_lat": "Русский латиницей",
    "kk": "Қазақша (кириллица)",
    "tr": "Türkçe",
    "de": "Deutsch",
    "zh": "中文",
}

PARALLEL = {
    "greeting": {
        "en": "Hello, world!",
        "ru": "Привет, мир!",
        "ru_lat": "Privet, mir!",
        "kk": "Сәлем, әлем!",
        "tr": "Merhaba, dünya!",
        "de": "Hallo, Welt!",
        "zh": "你好，世界！",
    },
    "ai": {
        "en": "Artificial intelligence is changing the world very fast.",
        "ru": "Искусственный интеллект очень быстро меняет мир.",
        "ru_lat": "Iskusstvennyj intellekt ochen bystro menyaet mir.",
        "kk": "Жасанды интеллект әлемді өте тез өзгертуде.",
        "tr": "Yapay zeka dünyayı çok hızlı değiştiriyor.",
        "de": "Künstliche Intelligenz verändert die Welt sehr schnell.",
        "zh": "人工智能正在飞速改变世界。",
    },
    "weather": {
        "en": "Today the weather is nice, so we decided to go for a walk in the park.",
        "ru": "Сегодня хорошая погода, поэтому мы решили погулять в парке.",
        "ru_lat": "Segodnya horoshaya pogoda, poetomu my reshili pogulyat v parke.",
        "kk": "Бүгін ауа райы жақсы, сондықтан біз саябақта серуендеуді шештік.",
        "tr": "Bugün hava güzel, bu yüzden parkta yürüyüşe çıkmaya karar verdik.",
        "de": "Heute ist das Wetter schön, deshalb haben wir beschlossen, im Park spazieren zu gehen.",
        "zh": "今天天气很好，所以我们决定去公园散步。",
    },
    "question": {
        "en": "What time does the train to Almaty leave tomorrow morning?",
        "ru": "Во сколько завтра утром отправляется поезд в Алматы?",
        "ru_lat": "Vo skolko zavtra utrom otpravlyaetsya poezd v Almaty?",
        "kk": "Ертең таңертең Алматыға пойыз сағат нешеде жүреді?",
        "tr": "Yarın sabah Almatı'ya giden tren saat kaçta kalkıyor?",
        "de": "Um wie viel Uhr fährt morgen früh der Zug nach Almaty ab?",
        "zh": "明天早上去阿拉木图的火车几点出发？",
    },
    "tokens_long": {
        "en": (
            "Large language models split text into tokens, and the number of "
            "tokens affects both the price and the context window."
        ),
        "ru": (
            "Большие языковые модели разбивают текст на токены, и количество "
            "токенов влияет и на цену, и на размер контекстного окна."
        ),
        "ru_lat": (
            "Bolshie yazykovye modeli razbivayut tekst na tokeny, i kolichestvo "
            "tokenov vliyaet i na tsenu, i na razmer kontekstnogo okna."
        ),
        "kk": (
            "Үлкен тілдік модельдер мәтінді токендерге бөледі, ал токендер "
            "саны бағаға да, контекстік терезенің өлшеміне де әсер етеді."
        ),
        "tr": (
            "Büyük dil modelleri metni token'lara böler ve token sayısı hem "
            "fiyatı hem de bağlam penceresini etkiler."
        ),
        "de": (
            "Große Sprachmodelle zerlegen Text in Token, und die Anzahl der "
            "Token beeinflusst sowohl den Preis als auch das Kontextfenster."
        ),
        "zh": "大语言模型会把文本拆分成词元，词元的数量会同时影响价格和上下文窗口。",
    },
    "paragraph": {
        "en": (
            "Coffee is one of the most popular drinks in the world. People drink it "
            "in the morning to wake up, at work to concentrate, and in the evening "
            "to meet friends. A good coffee shop is not only about the drink but "
            "also about the atmosphere."
        ),
        "ru": (
            "Кофе — один из самых популярных напитков в мире. Его пьют утром, чтобы "
            "проснуться, во время работы, чтобы сосредоточиться, и вечером, чтобы "
            "встретиться с друзьями. Хорошая кофейня — это не только напиток, но и "
            "атмосфера."
        ),
        "ru_lat": (
            "Kofe — odin iz samyh populyarnyh napitkov v mire. Ego pyut utrom, chtoby "
            "prosnutsya, vo vremya raboty, chtoby sosredotochitsya, i vecherom, chtoby "
            "vstretitsya s druzyami. Horoshaya kofeynya — eto ne tolko napitok, no i "
            "atmosfera."
        ),
        "kk": (
            "Кофе — әлемдегі ең танымал сусындардың бірі. Оны таңертең ояну үшін, "
            "жұмыс кезінде зейін қою үшін және кешке достармен кездесу үшін ішеді. "
            "Жақсы кофейня — тек сусын ғана емес, сонымен бірге атмосфера."
        ),
        "tr": (
            "Kahve dünyanın en popüler içeceklerinden biridir. İnsanlar onu sabahları "
            "uyanmak, çalışırken odaklanmak ve akşamları arkadaşlarıyla buluşmak için "
            "içer. İyi bir kahve dükkânı sadece içecekle değil, aynı zamanda "
            "atmosferle de ilgilidir."
        ),
        "de": (
            "Kaffee ist eines der beliebtesten Getränke der Welt. Man trinkt ihn "
            "morgens, um wach zu werden, bei der Arbeit, um sich zu konzentrieren, und "
            "abends, um Freunde zu treffen. Ein gutes Café ist nicht nur eine Frage "
            "des Getränks, sondern auch der Atmosphäre."
        ),
        "zh": (
            "咖啡是世界上最受欢迎的饮料之一。人们早上喝它来提神，工作时喝它来集中注意力，"
            "晚上喝它来和朋友见面。一家好的咖啡店不仅关乎饮品，也关乎氛围。"
        ),
    },
}

NEUTRAL = {
    "numbers": "Order #48213 was shipped on 2026-11-10 for $1,299.50 (VAT 12%), tracking 4006381333931.",
    "python": "def fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\nprint([fib(i) for i in range(10)])",
    "json": '{"user": {"id": 42, "name": "Kirill", "tags": ["llm", "tokens"], "active": true}}',
    "url": "https://github.com/mrOksenenko/llme_experements/blob/main/results/exp03.md?ref=main#L10",
    "emoji": "I love coffee ☕🔥 so much 😍👍🏽 #coffee #morning",
}
