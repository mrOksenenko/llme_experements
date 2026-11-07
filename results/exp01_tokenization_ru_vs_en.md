# Опыт 1. Токенизация: русский vs английский

Одна и та же мысль на двух языках, токенайзеры из `tiktoken` (`cl100k_base` — GPT-4, `o200k_base` — GPT-4o).

## Сводка

| Токенайзер | Фраза | EN токенов | RU токенов | RU/EN | EN симв/ток | RU симв/ток |
|---|---|---:|---:|---:|---:|---:|
| cl100k_base | main | 10 | 23 | 2.3x | 5.6 | 2.09 |
| cl100k_base | short | 4 | 7 | 1.75x | 3.25 | 1.71 |
| cl100k_base | long | 22 | 48 | 2.18x | 5.32 | 2.5 |
| o200k_base | main | 9 | 11 | 1.22x | 6.22 | 4.36 |
| o200k_base | short | 4 | 5 | 1.25x | 3.25 | 2.4 |
| o200k_base | long | 22 | 30 | 1.36x | 5.32 | 4.0 |

## Разбивка по токенам

### cl100k_base / main

**EN** — «Artificial intelligence is changing the world very fast.»  
10 токенов, 56 символов, 56 байт

`Art` `ificial` ` intelligence` ` is` ` changing` ` the` ` world` ` very` ` fast` `.`

**RU** — «Искусственный интеллект очень быстро меняет мир.»  
23 токенов, 48 символов, 90 байт

`И` `с` `ку` `с` `ств` `ен` `ный` ` ин` `т` `ел` `л` `ект` ` оч` `ень` ` бы` `стр` `о` ` мен` `я` `ет` ` м` `ир` `.`

### cl100k_base / short

**EN** — «Hello, world!»  
4 токенов, 13 символов, 13 байт

`Hello` `,` ` world` `!`

**RU** — «Привет, мир!»  
7 токенов, 12 символов, 21 байт

`Пр` `ив` `ет` `,` ` м` `ир` `!`

### cl100k_base / long

**EN** — «Large language models split text into tokens, and the number of tokens affects both the price and the context window.»  
22 токенов, 117 символов, 117 байт

`Large` ` language` ` models` ` split` ` text` ` into` ` tokens` `,` ` and` ` the` ` number` ` of` ` tokens` ` affects` ` both` ` the` ` price` ` and` ` the` ` context` ` window` `.`

**RU** — «Большие языковые модели разбивают текст на токены, и количество токенов влияет и на цену, и на размер контекстного окна.»  
48 токенов, 120 символов, 219 байт

`Б` `оль` `ши` `е` ` я` `з` `ы` `ков` `ые` ` мод` `ели` ` раз` `б` `ив` `а` `ют` ` текст` ` на` ` т` `ок` `ены` `,` ` и` ` количество` ` т` `ок` `ен` `ов` ` в` `ли` `я` `ет` ` и` ` на` ` ц` `ен` `у` `,` ` и` ` на` ` размер` ` конт` `ек` `ст` `ного` ` ок` `на` `.`

### o200k_base / main

**EN** — «Artificial intelligence is changing the world very fast.»  
9 токенов, 56 символов, 56 байт

`Artificial` ` intelligence` ` is` ` changing` ` the` ` world` ` very` ` fast` `.`

**RU** — «Искусственный интеллект очень быстро меняет мир.»  
11 токенов, 48 символов, 90 байт

`И` `ск` `ус` `ственный` ` интеллект` ` очень` ` быстро` ` меня` `ет` ` мир` `.`

### o200k_base / short

**EN** — «Hello, world!»  
4 токенов, 13 символов, 13 байт

`Hello` `,` ` world` `!`

**RU** — «Привет, мир!»  
5 токенов, 12 символов, 21 байт

`Пр` `ивет` `,` ` мир` `!`

### o200k_base / long

**EN** — «Large language models split text into tokens, and the number of tokens affects both the price and the context window.»  
22 токенов, 117 символов, 117 байт

`Large` ` language` ` models` ` split` ` text` ` into` ` tokens` `,` ` and` ` the` ` number` ` of` ` tokens` ` affects` ` both` ` the` ` price` ` and` ` the` ` context` ` window` `.`

**RU** — «Большие языковые модели разбивают текст на токены, и количество токенов влияет и на цену, и на размер контекстного окна.»  
30 токенов, 120 символов, 219 байт

`Больш` `ие` ` язы` `ковые` ` модели` ` разб` `ивают` ` текст` ` на` ` ток` `ены` `,` ` и` ` количество` ` ток` `ен` `ов` ` влияет` ` и` ` на` ` цену` `,` ` и` ` на` ` размер` ` конт` `екст` `ного` ` окна` `.`
