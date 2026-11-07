"""Опыт 2: случайность. Один промпт, три независимых «чата».

Промпт: «Придумай название для кофейни»
Каждый прогон — отдельный субагент Claude с чистым контекстом (аналог нового чата),
модель — Sonnet 5.5, температура по умолчанию. Ответы собраны вручную в DATA ниже
(полный текст — results/exp02_raw_answers.md), скрипт считает совпадения.

Запуск:  python3 exp02_randomness_coffee_names.py
Результат: results/exp02_randomness_coffee_names.md (+ .json)
"""
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

PROMPT = "Придумай название для кофейни"

DATA = {
    "chat1": {
        "names": [
            "Зерно", "Крема", "Тёплый угол", "Утро в чашке",
            "Ристретто", "Обжарка №1", "Кофе и точка", "Ещё по одной",
            "Бариста Бар", "Чёрная пятница", "Арабика Club", "Пенка",
        ],
        "picks": ["Зерно", "Тёплый угол"],
    },
    "chat2": {
        "names": [
            "Зерно & Ко", "Кружка", "Тёплый берег", "Обжарка №7",
            "Крема", "Ристретто", "Кофе на посошок", "Эспрессо Патронум",
            "Утро добрым не бывает", "Bean There", "Daily Grind", "Slow Pour",
        ],
        "picks": ["Зерно & Ко", "Крема"],
    },
    "chat3": {
        "names": [
            "Зерно & Плед", "Третья чашка", "Тёплый угол", "Обжарка",
            "Ристретто", "Крема", "Кофе-пауза", "Ещё по одной",
            "Бодрый четверг", "Brew Nook", "Mokka", "Bean There",
        ],
        "picks": ["Третья чашка"],
    },
}

# «Семейства»: названия с общим корнем идеи (подбор вручную)
FAMILIES = {
    "Зерно*": ["Зерно", "Зерно & Ко", "Зерно & Плед"],
    "Обжарка*": ["Обжарка №1", "Обжарка №7", "Обжарка"],
    "Тёплый*": ["Тёплый угол", "Тёплый берег"],
}


def norm(s):
    return s.lower().replace("ё", "е").strip()


def main():
    chats = list(DATA)
    all_names = [n for c in chats for n in DATA[c]["names"]]

    # Точные совпадения
    where = defaultdict(list)
    for c in chats:
        for n in DATA[c]["names"]:
            where[norm(n)].append(c)
    display = {norm(n): n for c in chats for n in DATA[c]["names"]}
    exact = {display[k]: v for k, v in where.items() if len(v) > 1}

    # Семейства
    fam_hits = {}
    for fam, members in FAMILIES.items():
        m = {norm(x) for x in members}
        fam_hits[fam] = sorted({c for c in chats for n in DATA[c]["names"] if norm(n) in m})

    # Жаккар по парам чатов (точные совпадения)
    jacc = {}
    for a, b in combinations(chats, 2):
        sa = {norm(n) for n in DATA[a]["names"]}
        sb = {norm(n) for n in DATA[b]["names"]}
        jacc[f"{a}-{b}"] = round(len(sa & sb) / len(sa | sb), 2)

    summary = {
        "prompt": PROMPT,
        "total_names": len(all_names),
        "unique_names": len({norm(n) for n in all_names}),
        "exact_repeats": exact,
        "family_hits": fam_hits,
        "jaccard_pairs": jacc,
        "picks": {c: DATA[c]["picks"] for c in chats},
        "data": DATA,
    }

    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "exp02_randomness_coffee_names.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [f"# Опыт 2. Случайность: «{PROMPT}» ×3\n"]
    md.append(
        "Один и тот же промпт, три независимых запуска с чистым контекстом "
        "(новый «чат» = отдельный субагент Claude Sonnet 5.5, температура по умолчанию). "
        "Полные ответы: [exp02_raw_answers.md](exp02_raw_answers.md).\n"
    )
    md.append("## Цифры\n")
    md.append(f"- Всего названий: **{summary['total_names']}** (по 12 в каждом чате)")
    md.append(f"- Уникальных (точное совпадение): **{summary['unique_names']}**")
    md.append(f"- Повторов: **{summary['total_names'] - summary['unique_names']}**\n")
    md.append("## Названия, повторившиеся дословно\n")
    md.append("| Название | В каких чатах |")
    md.append("|---|---|")
    for n, v in sorted(exact.items(), key=lambda kv: -len(kv[1])):
        md.append(f"| {n} | {', '.join(v)} ({len(v)}/3) |")
    md.append("\n## Повторяющиеся идеи (общий корень)\n")
    md.append("| Семейство | Варианты | В каких чатах |")
    md.append("|---|---|---|")
    for fam, members in FAMILIES.items():
        md.append(f"| {fam} | {', '.join(members)} | {', '.join(fam_hits[fam])} ({len(fam_hits[fam])}/3) |")
    md.append("\n## Сходство пар чатов (индекс Жаккара по точным совпадениям)\n")
    md.append("| Пара | Жаккар |")
    md.append("|---|---:|")
    for k, v in jacc.items():
        md.append(f"| {k} | {v} |")
    md.append("\n## Что каждый чат выбрал как лучшее\n")
    for c in chats:
        md.append(f"- **{c}**: {', '.join('«' + p + '»' for p in DATA[c]['picks'])}")
    md.append("")
    (out / "exp02_randomness_coffee_names.md").write_text("\n".join(md), encoding="utf-8")

    print(f"всего={summary['total_names']} уникальных={summary['unique_names']}")
    print("дословные повторы:", exact)
    print("семейства:", fam_hits)
    print("жаккар:", jacc)


if __name__ == "__main__":
    main()
