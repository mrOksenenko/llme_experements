"""Опыт 1: одна и та же фраза на разных языках/письменностях через токенайзер.

Языки: английский (база), русский (кириллица), русский латиницей (транслит),
казахский (кириллица), китайский.
Токенайзеры: все, что собирает exp03 (GPT-4, GPT-4o, Qwen3, Gemma 3, Llama 4,
Claude 1/2 legacy; актуальные Claude добавляются при наличии ANTHROPIC_API_KEY).

Запуск:  .venv/bin/python exp01_tokenization_ru_vs_en.py
Результат: results/exp01_tokenization_ru_vs_en.md (+ .json)
"""
import json
from pathlib import Path

from corpus import LANGS as ALL_LANGS
from corpus import PARALLEL
from exp03_tokenizers_multi import build_counters

# Порядок важен: первый язык — база для сравнения
LANGS = {k: ALL_LANGS[k] for k in ("en", "ru", "ru_lat", "kk", "zh")}

# Три фразы из общего корпуса: короткая, средняя, длинная
PHRASES = [("short", "greeting"), ("main", "ai"), ("long", "tokens_long")]


def main():
    counters, notes = build_counters()
    base = next(iter(LANGS))
    results = []
    for name, count in counters.items():
        for phrase_name, corpus_key in PHRASES:
            row = {"encoding": name, "phrase": phrase_name, "langs": {}}
            for lang in LANGS:
                text = PARALLEL[corpus_key][lang]
                n, pieces = count(text, want_pieces=True)
                row["langs"][lang] = {
                    "text": text,
                    "tokens": n,
                    "chars": len(text),
                    "bytes_utf8": len(text.encode("utf-8")),
                    "chars_per_token": round(len(text) / n, 2),
                    "pieces": pieces,
                }
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
        "(транслит), казахском и китайском. Токенайзеры: " + ", ".join(counters) + ". "
        "В скобках — отношение к английскому.\n"
    )
    for x in notes:
        md.append(f"> {x}\n")
    md.append("## Сводка: число токенов\n")
    head = "| Токенайзер | Фраза | " + " | ".join(LANGS.values()) + " |"
    md += [head, "|---|---|" + "---:|" * len(LANGS)]
    for r in results:
        cells = []
        for lang in LANGS:
            d = r["langs"][lang]
            cells.append(f"{d['tokens']}" if lang == base else f"{d['tokens']} ({d['ratio_to_en']}x)")
        md.append(f"| {r['encoding']} | {r['phrase']} | " + " | ".join(cells) + " |")

    md.append("\n## Сводка: символов на токен\n")
    md += [head, "|---|---|" + "---:|" * len(LANGS)]
    for r in results:
        cells = [str(r["langs"][lang]["chars_per_token"]) for lang in LANGS]
        md.append(f"| {r['encoding']} | {r['phrase']} | " + " | ".join(cells) + " |")

    md.append("\n## Разбивка по токенам\n")
    for r in results:
        md.append(f"### {r['encoding']} / {r['phrase']}\n")
        for lang, title in LANGS.items():
            d = r["langs"][lang]
            if d["pieces"] is None:
                shown = "(разбивка недоступна)"
            else:
                shown = " ".join(f"`{s}`" if s.strip() else f"`{s!r}`" for s in d["pieces"])
            md.append(
                f"**{title}** — «{d['text']}»  \n"
                f"{d['tokens']} токенов, {d['chars']} символов, {d['bytes_utf8']} байт\n\n"
                f"{shown}\n"
            )
    (out / "exp01_tokenization_ru_vs_en.md").write_text("\n".join(md), encoding="utf-8")

    for r in results:
        line = "  ".join(
            f"{lang}={r['langs'][lang]['tokens']:3}({r['langs'][lang]['ratio_to_en']}x)"
            for lang in LANGS
        )
        print(f"{r['encoding']:20} {r['phrase']:6} {line}")


if __name__ == "__main__":
    main()
