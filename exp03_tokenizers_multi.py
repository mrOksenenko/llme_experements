"""Опыт 3: расширенное сравнение токенайзеров на 7 языках + «нейтральных» текстах.

Токенайзеры:
  - OpenAI (tiktoken): cl100k_base (GPT-4), o200k_base (GPT-4o)
  - Свежие открытые модели (Hugging Face tokenizer.json): Qwen3, Gemma 3, Llama 4
  - Anthropic Claude: токенайзер закрытый, число токенов считается через API
    (messages.count_tokens). Нужен ANTHROPIC_API_KEY в окружении; без ключа этот
    блок пропускается.

Запуск:
    .venv/bin/python exp03_tokenizers_multi.py
    ANTHROPIC_API_KEY=... .venv/bin/python exp03_tokenizers_multi.py   # + Claude

Результат: results/exp03_tokenizers.md, results/exp03_tokenizers.json,
           results/exp03_pieces_ai.md (разбивка предложения про ИИ на токены)
"""
import json
import os
import statistics
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from corpus import LANGS, NEUTRAL, PARALLEL

# (вид, идентификатор, подпись)
TOKENIZERS = [
    ("tiktoken", "cl100k_base", "GPT-4 (cl100k)"),
    ("tiktoken", "o200k_base", "GPT-4o (o200k)"),
    ("hf", "Qwen/Qwen3-8B", "Qwen3"),
    ("hf", "unsloth/gemma-3-4b-it", "Gemma 3"),  # зеркало токенайзера google/gemma-3
    ("hf", "unsloth/Llama-4-Scout-17B-16E-Instruct", "Llama 4"),  # зеркало meta-llama
]

# Модели Claude для count_tokens (у разных поколений токенайзер может отличаться)
ANTHROPIC_MODELS = [
    ("claude-fable-5-1", "Claude Fable 5.1"),
    ("claude-opus-5-5", "Claude Opus 5.5"),
    ("claude-sonnet-5-5", "Claude Sonnet 5.5"),
    ("claude-haiku-5-5", "Claude Haiku 5.5"),
]


def hf_counter(repo):
    from huggingface_hub import hf_hub_download
    from tokenizers import Tokenizer

    tok = Tokenizer.from_file(hf_hub_download(repo, "tokenizer.json"))

    def count(text, want_pieces=False):
        ids = tok.encode(text, add_special_tokens=False).ids
        pieces = [tok.decode([i]) for i in ids] if want_pieces else None
        return len(ids), pieces

    return count


def tiktoken_counter(name):
    import tiktoken

    enc = tiktoken.get_encoding(name)

    def count(text, want_pieces=False):
        ids = enc.encode(text)
        pieces = None
        if want_pieces:
            pieces = []
            for i in ids:
                raw = enc.decode_single_token_bytes(i)
                try:
                    pieces.append(raw.decode("utf-8"))
                except UnicodeDecodeError:
                    pieces.append("".join(f"\\x{b:02x}" for b in raw))
        return len(ids), pieces

    return count


def anthropic_counter(client, model):
    """count_tokens считает токены всего сообщения (с обвязкой роли).
    Обвязку вычитаем: overhead = count("a") - 1."""

    def raw(text):
        r = client.messages.count_tokens(
            model=model, messages=[{"role": "user", "content": text}]
        )
        return r.input_tokens

    overhead = raw("a") - 1

    def count(text, want_pieces=False):
        return raw(text) - overhead, None

    return count


def build_counters():
    counters, notes = {}, []
    for kind, ident, label in TOKENIZERS:
        try:
            counters[label] = (
                tiktoken_counter(ident) if kind == "tiktoken" else hf_counter(ident)
            )
        except Exception as e:  # noqa: BLE001
            notes.append(f"{label}: не загрузился ({type(e).__name__}: {str(e)[:80]})")
    if os.environ.get("ANTHROPIC_API_KEY"):
        import anthropic

        client = anthropic.Anthropic()
        for model, label in ANTHROPIC_MODELS:
            try:
                counters[label] = anthropic_counter(client, model)
            except Exception as e:  # noqa: BLE001
                notes.append(f"{label} ({model}): ошибка API ({type(e).__name__}: {str(e)[:80]})")
    else:
        notes.append("Anthropic Claude: пропущено — не задан ANTHROPIC_API_KEY")
    return counters, notes


def main():
    counters, notes = build_counters()
    names = list(counters)
    langs = list(LANGS)

    # --- подсчёт ---
    parallel = {t: {n: {} for n in names} for t in PARALLEL}
    neutral = {t: {} for t in NEUTRAL}
    for t, texts in PARALLEL.items():
        for n in names:
            for lang in langs:
                parallel[t][n][lang] = counters[n](texts[lang])[0]
    for t, text in NEUTRAL.items():
        for n in names:
            neutral[t][n] = counters[n](text)[0]

    # --- агрегаты по языку ---
    ratio, total = {}, {}
    for n in names:
        ratio[n], total[n] = {}, {}
        for lang in langs:
            ratio[n][lang] = round(
                statistics.mean(parallel[t][n][lang] / parallel[t][n]["en"] for t in PARALLEL), 2
            )
            total[n][lang] = sum(parallel[t][n][lang] for t in PARALLEL)

    # --- JSON ---
    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "exp03_tokenizers.json").write_text(
        json.dumps(
            {
                "tokenizers": names,
                "notes": notes,
                "mean_ratio_to_en": ratio,
                "total_tokens": total,
                "parallel": parallel,
                "neutral": neutral,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --- Markdown ---
    head = "| Токенайзер | " + " | ".join(LANGS.values()) + " |"
    sep = "|---|" + "---:|" * len(langs)
    md = ["# Опыт 3. Токенайзеры: 7 языков × свежие модели\n"]
    md.append(
        f"Корпус: {len(PARALLEL)} параллельных текстов на {len(langs)} языках/письменностях "
        f"и {len(NEUTRAL)} нейтральных (числа, код, JSON, URL, эмодзи). "
        "Токенайзеры: OpenAI (`tiktoken`), Qwen3, Gemma 3, Llama 4 (Hugging Face)"
        + (", Claude (API `count_tokens`)." if any(n.startswith("Claude") for n in names) else ".")
        + "\n"
    )
    if notes:
        md.append("**Примечания:**\n")
        md += [f"- {x}" for x in notes]
        md.append("")

    md.append("## 1. Главное: во сколько раз язык дороже английского\n")
    md.append("Среднее отношение числа токенов к английскому по всем параллельным текстам. 1.00 = как английский.\n")
    md += [head, sep]
    for n in names:
        md.append(f"| {n} | " + " | ".join(f"{ratio[n][l]:.2f}x" for l in langs) + " |")

    md.append("\n## 2. Сумма токенов по всем параллельным текстам\n")
    md += [head, sep]
    for n in names:
        md.append(f"| {n} | " + " | ".join(str(total[n][l]) for l in langs) + " |")

    md.append("\n## 3. По каждому тексту\n")
    for t, texts in PARALLEL.items():
        md.append(f"### {t}\n")
        md += [head, sep]
        for n in names:
            md.append(f"| {n} | " + " | ".join(str(parallel[t][n][l]) for l in langs) + " |")
        md.append("")
    md.append("Исходные тексты: [corpus.py](../corpus.py).\n")

    md.append("## 4. Нейтральные тексты (число токенов / число символов)\n")
    md.append("| Токенайзер | " + " | ".join(f"{t} ({len(NEUTRAL[t])})" for t in NEUTRAL) + " |")
    md.append("|---|" + "---:|" * len(NEUTRAL))
    for n in names:
        md.append(f"| {n} | " + " | ".join(str(neutral[t][n]) for t in NEUTRAL) + " |")
    md.append("")
    (out / "exp03_tokenizers.md").write_text("\n".join(md), encoding="utf-8")

    # --- разбивка предложения про ИИ ---
    pm = ["# Опыт 3. Разбивка предложения «ai» на токены\n"]
    for lang, title in LANGS.items():
        pm.append(f"## {title}\n\n«{PARALLEL['ai'][lang]}»\n")
        for n in names:
            cnt, pieces = counters[n](PARALLEL["ai"][lang], want_pieces=True)
            if pieces is None:
                pm.append(f"- **{n}**: {cnt} токенов (разбивка недоступна, токенайзер закрытый)")
            else:
                shown = " ".join(f"`{p}`" if p.strip() else f"`{p!r}`" for p in pieces)
                pm.append(f"- **{n}** ({cnt}): {shown}")
        pm.append("")
    (out / "exp03_pieces_ai.md").write_text("\n".join(pm), encoding="utf-8")

    # --- консоль ---
    print("Среднее отношение к английскому:")
    print(f"{'':20}" + "".join(f"{l:>8}" for l in langs))
    for n in names:
        print(f"{n:20}" + "".join(f"{ratio[n][l]:>7.2f}x" for l in langs))
    for x in notes:
        print("!", x, file=sys.stderr)


if __name__ == "__main__":
    main()
