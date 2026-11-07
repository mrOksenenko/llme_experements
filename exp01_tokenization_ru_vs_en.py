"""Опыт 1: одна и та же фраза на русском и английском через токенайзер.

Запуск:  .venv/bin/python exp01_tokenization_ru_vs_en.py
Результат: results/exp01_tokenization_ru_vs_en.md (+ .json)
"""
import json
from pathlib import Path

import tiktoken

# Пары «одна и та же мысль» на двух языках
PHRASES = [
    {
        "name": "main",
        "en": "Artificial intelligence is changing the world very fast.",
        "ru": "Искусственный интеллект очень быстро меняет мир.",
    },
    {
        "name": "short",
        "en": "Hello, world!",
        "ru": "Привет, мир!",
    },
    {
        "name": "long",
        "en": (
            "Large language models split text into tokens, and the number of "
            "tokens affects both the price and the context window."
        ),
        "ru": (
            "Большие языковые модели разбивают текст на токены, и количество "
            "токенов влияет и на цену, и на размер контекстного окна."
        ),
    },
]

ENCODINGS = ["cl100k_base", "o200k_base"]  # GPT-4 / GPT-4o


def show(enc, token_id):
    """Читаемый вид токена: для неполных UTF-8 байтов показываем \\x.."""
    raw = enc.decode_single_token_bytes(token_id)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return "".join(f"\\x{b:02x}" for b in raw)


def analyze(enc, text):
    ids = enc.encode(text)
    return {
        "tokens": len(ids),
        "chars": len(text),
        "bytes_utf8": len(text.encode("utf-8")),
        "chars_per_token": round(len(text) / len(ids), 2),
        "pieces": [show(enc, i) for i in ids],
    }


def main():
    results = []
    for enc_name in ENCODINGS:
        enc = tiktoken.get_encoding(enc_name)
        for p in PHRASES:
            en, ru = analyze(enc, p["en"]), analyze(enc, p["ru"])
            results.append(
                {
                    "encoding": enc_name,
                    "phrase": p["name"],
                    "text_en": p["en"],
                    "text_ru": p["ru"],
                    "en": en,
                    "ru": ru,
                    "ratio_ru_to_en": round(ru["tokens"] / en["tokens"], 2),
                }
            )

    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "exp01_tokenization_ru_vs_en.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = ["# Опыт 1. Токенизация: русский vs английский\n"]
    md.append(
        "Одна и та же мысль на двух языках, токенайзеры из `tiktoken` "
        "(`cl100k_base` — GPT-4, `o200k_base` — GPT-4o).\n"
    )
    md.append("## Сводка\n")
    md.append("| Токенайзер | Фраза | EN токенов | RU токенов | RU/EN | EN симв/ток | RU симв/ток |")
    md.append("|---|---|---:|---:|---:|---:|---:|")
    for r in results:
        md.append(
            f"| {r['encoding']} | {r['phrase']} | {r['en']['tokens']} | "
            f"{r['ru']['tokens']} | {r['ratio_ru_to_en']}x | "
            f"{r['en']['chars_per_token']} | {r['ru']['chars_per_token']} |"
        )
    md.append("\n## Разбивка по токенам\n")
    for r in results:
        md.append(f"### {r['encoding']} / {r['phrase']}\n")
        for lang in ("en", "ru"):
            d = r[lang]
            pieces = " ".join(f"`{s}`" if s.strip() else f"`{s!r}`" for s in d["pieces"])
            md.append(
                f"**{lang.upper()}** — «{r['text_' + lang]}»  \n"
                f"{d['tokens']} токенов, {d['chars']} символов, {d['bytes_utf8']} байт\n\n"
                f"{pieces}\n"
            )
    (out / "exp01_tokenization_ru_vs_en.md").write_text("\n".join(md), encoding="utf-8")

    # Краткий вывод в консоль
    for r in results:
        print(
            f"{r['encoding']:12} {r['phrase']:6} EN={r['en']['tokens']:3}  "
            f"RU={r['ru']['tokens']:3}  RU/EN={r['ratio_ru_to_en']}x"
        )


if __name__ == "__main__":
    main()
