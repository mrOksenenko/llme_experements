"""Опыт 1: одна и та же фраза на разных языках/письменностях через токенайзер.

Языки: английский (база), русский (кириллица), русский латиницей (транслит),
казахский (кириллица).

Запуск:  .venv/bin/python exp01_tokenization_ru_vs_en.py
Результат: results/exp01_tokenization_ru_vs_en.md (+ .json)
"""
import json
from pathlib import Path

import tiktoken

# Порядок важен: первый язык — база для сравнения
LANGS = {
    "en": "Английский",
    "ru": "Русский (кириллица)",
    "ru_lat": "Русский латиницей",
    "kk": "Казахский (кириллица)",
}

# Одна и та же мысль на всех языках
PHRASES = [
    {
        "name": "main",
        "en": "Artificial intelligence is changing the world very fast.",
        "ru": "Искусственный интеллект очень быстро меняет мир.",
        "ru_lat": "Iskusstvennyj intellekt ochen bystro menyaet mir.",
        "kk": "Жасанды интеллект әлемді өте тез өзгертуде.",
    },
    {
        "name": "short",
        "en": "Hello, world!",
        "ru": "Привет, мир!",
        "ru_lat": "Privet, mir!",
        "kk": "Сәлем, әлем!",
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
        "ru_lat": (
            "Bolshie yazykovye modeli razbivayut tekst na tokeny, i kolichestvo "
            "tokenov vliyaet i na tsenu, i na razmer kontekstnogo okna."
        ),
        "kk": (
            "Үлкен тілдік модельдер мәтінді токендерге бөледі, ал токендер "
            "саны бағаға да, контекстік терезенің өлшеміне де әсер етеді."
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
        "text": text,
        "tokens": len(ids),
        "chars": len(text),
        "bytes_utf8": len(text.encode("utf-8")),
        "chars_per_token": round(len(text) / len(ids), 2),
        "pieces": [show(enc, i) for i in ids],
    }


def main():
    base = next(iter(LANGS))
    results = []
    for enc_name in ENCODINGS:
        enc = tiktoken.get_encoding(enc_name)
        for p in PHRASES:
            row = {"encoding": enc_name, "phrase": p["name"], "langs": {}}
            for lang in LANGS:
                row["langs"][lang] = analyze(enc, p[lang])
            b = row["langs"][base]["tokens"]
            for lang in LANGS:
                row["langs"][lang]["ratio_to_en"] = round(row["langs"][lang]["tokens"] / b, 2)
            results.append(row)

    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "exp01_tokenization_ru_vs_en.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = ["# Опыт 1. Токенизация: одна фраза на разных языках\n"]
    md.append(
        "Одна и та же мысль на английском, русском (кириллица), русском латиницей "
        "(транслит) и казахском. Токенайзеры из `tiktoken`: `cl100k_base` — GPT-4, "
        "`o200k_base` — GPT-4o. В скобках — отношение к английскому.\n"
    )
    md.append("## Сводка: число токенов\n")
    head = "| Токенайзер | Фраза | " + " | ".join(LANGS.values()) + " |"
    md.append(head)
    md.append("|---|---|" + "---:|" * len(LANGS))
    for r in results:
        cells = []
        for lang in LANGS:
            d = r["langs"][lang]
            cells.append(f"{d['tokens']}" if lang == base else f"{d['tokens']} ({d['ratio_to_en']}x)")
        md.append(f"| {r['encoding']} | {r['phrase']} | " + " | ".join(cells) + " |")

    md.append("\n## Сводка: символов на токен\n")
    md.append(head)
    md.append("|---|---|" + "---:|" * len(LANGS))
    for r in results:
        cells = [str(r["langs"][lang]["chars_per_token"]) for lang in LANGS]
        md.append(f"| {r['encoding']} | {r['phrase']} | " + " | ".join(cells) + " |")

    md.append("\n## Разбивка по токенам\n")
    for r in results:
        md.append(f"### {r['encoding']} / {r['phrase']}\n")
        for lang, title in LANGS.items():
            d = r["langs"][lang]
            pieces = " ".join(f"`{s}`" if s.strip() else f"`{s!r}`" for s in d["pieces"])
            md.append(
                f"**{title}** — «{d['text']}»  \n"
                f"{d['tokens']} токенов, {d['chars']} символов, {d['bytes_utf8']} байт\n\n"
                f"{pieces}\n"
            )
    (out / "exp01_tokenization_ru_vs_en.md").write_text("\n".join(md), encoding="utf-8")

    # Краткий вывод в консоль
    for r in results:
        line = "  ".join(
            f"{lang}={r['langs'][lang]['tokens']:3}({r['langs'][lang]['ratio_to_en']}x)"
            for lang in LANGS
        )
        print(f"{r['encoding']:12} {r['phrase']:6} {line}")


if __name__ == "__main__":
    main()
