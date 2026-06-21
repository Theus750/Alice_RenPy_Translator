import hashlib
from pathlib import Path
from typing import Dict, List

from .translation_entry import TranslationEntry


def _escape_renpy(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _label_from_context(context_path: str) -> str | None:
    if not context_path.startswith("label:"):
        return None
    first_segment = context_path.split(" > ", 1)[0]
    return first_segment.split(":", 1)[1]


def _encode_say_string(text: str) -> str:
    encoded = text.replace("\\", "\\\\")
    encoded = encoded.replace("\n", "\\n")
    encoded = encoded.replace('"', '\\"')
    encoded = encoded.replace("  ", " \\ ")
    return f'"{encoded}"'


def _dialogue_code(entry: TranslationEntry, text: str) -> str:
    encoded = _encode_say_string(text)
    if entry.entry_type == "dialogue" and entry.speaker:
        return f"{entry.speaker} {encoded}"
    return encoded


def _replace_first_string_literal(code: str, text: str) -> str:
    for quote in ('"', "'"):
        start = code.find(quote)
        if start == -1:
            continue

        i = start + 1
        while i < len(code):
            if code[i] == "\\":
                i += 2
                continue
            if code[i] == quote:
                escaped = text.replace("\\", "\\\\").replace("\n", "\\n")
                if quote == '"':
                    escaped = escaped.replace('"', '\\"')
                else:
                    escaped = escaped.replace("'", "\\'")
                return code[: start + 1] + escaped + code[i:]
            i += 1

    return code


def _translated_dialogue_code(entry: TranslationEntry, text: str) -> str:
    raw_code = entry.raw_code or ""
    if '("' in raw_code or "('" in raw_code:
        return _replace_first_string_literal(raw_code, text)
    return _dialogue_code(entry, text)


def _dialogue_identifier(entry: TranslationEntry, used_identifiers: set[str]) -> str | None:
    label = _label_from_context(entry.context_path)
    if not label:
        return None

    digest = hashlib.md5(
        (_dialogue_code(entry, entry.original_text) + "\r\n").encode("utf-8")
    ).hexdigest()[:8]
    base = f"{label.replace('.', '_')}_{digest}"
    identifier = base
    suffix = 0

    while identifier in used_identifiers:
        suffix += 1
        identifier = f"{base}_{suffix}"

    used_identifiers.add(identifier)
    return identifier


def save_dialogue_rpy(
    entries: List[TranslationEntry],
    translations_by_id: Dict[str, str],
    language: str = "portuguese",
    output_path: str = "game/tl/portuguese/dialogue.rpy",
) -> Path:
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append("# Arquivo de traducao de dialogos")
    lines.append("# Gerado automaticamente\n")
    used_identifiers: set[str] = set()

    for entry in sorted(entries, key=lambda item: (item.file_path, item.line_number)):
        if entry.entry_type not in {"dialogue", "narration"}:
            continue

        identifier = _dialogue_identifier(entry, used_identifiers)
        if not identifier:
            continue

        original_code = entry.raw_code or _dialogue_code(entry, entry.original_text)
        translated = translations_by_id.get(entry.translation_id, entry.original_text)
        translated_code = _translated_dialogue_code(entry, translated)

        lines.append(f"# {entry.file_path}:{entry.line_number}")
        lines.append(f"translate {language} {identifier}:")
        lines.append("")
        lines.append(f"    # {original_code}")
        lines.append(f"    {translated_code}")
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file


def save_strings_rpy(
    entries: List[TranslationEntry],
    translations_by_id: Dict[str, str],
    language: str = "portuguese",
    output_path: str = "game/tl/portuguese/strings.rpy",
) -> Path:
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = [f"translate {language} strings:", ""]
    seen: set[str] = set()

    for entry in sorted(entries, key=lambda item: (item.file_path, item.line_number)):
        if entry.entry_type != "menu_choice":
            continue
        if entry.original_text in seen:
            continue

        seen.add(entry.original_text)
        old = _escape_renpy(entry.original_text)
        new = _escape_renpy(translations_by_id.get(entry.translation_id, entry.original_text))
        lines.append(f'    old "{old}"')
        lines.append(f'    new "{new}"')
        lines.append("")

    out_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_file


def save_language_rpy(
    language: str,
    output_path: str,
) -> Path:
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = [
        "# Arquivo de ativacao de idioma gerado automaticamente",
        f'define config.language = "{language}"',
        "",
    ]

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file
