import os
import re


def parse_markdown(filepath: str) -> list[dict]:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    source_file = os.path.basename(filepath)
    raw_chunks = content.split("\n---\n")
    results = []

    for raw in raw_chunks:
        raw = raw.strip()
        if not raw:
            continue

        chunk = _parse_chunk(raw, source_file)
        results.append(chunk)

    return results


def _parse_chunk(text: str, source_file: str) -> dict:
    sections = {
        "trigger": "",
        "fact": "",
        "insight": "",
        "quest_seed": "",
    }

    heading_map = {
        "トリガー": "trigger",
        "表層知識": "fact",
        "深層知識": "insight",
        "クエストの種": "quest_seed",
    }

    pattern = r"^## (" + "|".join(heading_map.keys()) + r")\s*$"
    parts = re.split(pattern, text, flags=re.MULTILINE)

    # parts: [before_first_heading, heading1, content1, heading2, content2, ...]
    i = 1
    while i < len(parts) - 1:
        heading = parts[i]
        body = parts[i + 1].strip()
        key = heading_map.get(heading)
        if key:
            sections[key] = body
        i += 2

    for required in ("trigger", "fact", "insight"):
        if not sections[required]:
            raise ValueError(
                f"{source_file}: チャンク内に必須セクション「{required}」が空です"
            )

    return {
        "trigger": sections["trigger"],
        "fact": sections["fact"],
        "insight": sections["insight"],
        "quest_seed": sections["quest_seed"],
        "source_file": source_file,
    }
