from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from translation_entry import TranslationEntry


def _escape_renpy(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _label_from_context(context_path: str) -> str | None:
    if not context_path.startswith("label:"):
        return None
    first_segment = context_path.split(" > ", 1)[0]
    return first_segment.split(":", 1)[1]


def save_dialogue_rpy(
    entries: List[TranslationEntry],
    translations_by_id: Dict[str, str],
    language: str = "portuguese",
    output_path: str = "game/tl/portuguese/dialogue.rpy",
) -> Path:
    grouped: dict[str, list[TranslationEntry]] = defaultdict(list)
    for entry in sorted(entries, key=lambda item: (item.file_path, item.line_number)):
        if entry.entry_type not in {"dialogue", "narration"}:
            continue
        label = _label_from_context(entry.context_path)
        if not label:
            continue
        grouped[label].append(entry)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append("# Arquivo de tradução de diálogos")
    lines.append("# Gerado automaticamente\n")

    for label in sorted(grouped.keys()):
        lines.append(f"translate {language} {label}:")
        lines.append("")

        for entry in grouped[label]:
            translated = translations_by_id.get(entry.translation_id, entry.original_text)
            escaped = _escape_renpy(translated)
            if entry.entry_type == "dialogue" and entry.speaker:
                lines.append(f'    {entry.speaker} "{escaped}"')
            else:
                lines.append(f'    "{escaped}"')

        if not grouped[label]:
            lines.append("    pass")
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file
