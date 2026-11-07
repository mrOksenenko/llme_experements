# llme_experements

Опыты с LLM. Каждый опыт — скрипт `expNN_*.py` + отчёт в `results/`.

## Окружение

```bash
python3 -m venv .venv
.venv/bin/pip install tiktoken
```

## Опыты

| # | Опыт | Скрипт | Отчёт |
|---|------|--------|-------|
| 1 | Токенизация одной фразы: русский vs английский | `exp01_tokenization_ru_vs_en.py` | [results/exp01_tokenization_ru_vs_en.md](results/exp01_tokenization_ru_vs_en.md) |

### Опыт 1 — главный результат

На `cl100k_base` (GPT-4) русский текст занимает в ~1.8–2.3 раза больше токенов, чем английский;
на `o200k_base` (GPT-4o) разрыв сокращается до ~1.2–1.4 раза.
