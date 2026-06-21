import json
import re
from pathlib import Path
from typing import Iterable, List

from .translation_entry import TranslationEntry, build_translation_id


LABEL_PATTERN = re.compile(r"^\s*label\s+([A-Za-z_]\w*)\s*:")
BLOCK_PATTERN = re.compile(r"^\s*(menu|if|elif|else|while|for)\b(.*):\s*$")
DIALOGUE_PATTERN = re.compile(
    r'^\s*([A-Za-z_]\w*)\s+(?:'
    r'"((?:[^"\\]|\\.)*)"|'
    r'\(\s*"((?:[^"\\]|\\.)*)"\s*\)|'
    r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)|'
    r'\(\s*_\(\s*"((?:[^"\\]|\\.)*)"\s*\)\s*\)|'
    r"_\(\s*'((?:[^'\\]|\\.)*)'\s*\)|"
    r"\(\s*_\(\s*'((?:[^'\\]|\\.)*)'\s*\)\s*\)"
    r')\s*(?:#.*)?$'
)
SCREEN_LANGUAGE_KEYWORDS = {
    "add",
    "bar",
    "button",
    "fixed",
    "frame",
    "grid",
    "hbox",
    "id",
    "imagebutton",
    "input",
    "key",
    "null",
    "side",
    "text",
    "textbutton",
    "timer",
    "transform",
    "vbox",
    "viewport",
    "window",
}
NARRATOR_PATTERN = re.compile(
    r'^\s*(?:'
    r'"((?:[^"\\]|\\.)*)"|'
    r'\(\s*"((?:[^"\\]|\\.)*)"\s*\)|'
    r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)|'
    r'\(\s*_\(\s*"((?:[^"\\]|\\.)*)"\s*\)\s*\)|'
    r"_\(\s*'((?:[^'\\]|\\.)*)'\s*\)|"
    r"\(\s*_\(\s*'((?:[^'\\]|\\.)*)'\s*\)\s*\)"
    r')\s*(?:#.*)?$'
)
MENU_CHOICE_PATTERN = re.compile(
    r'^\s*(?:'
    r'"((?:[^"\\]|\\.)*)"|'
    r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)|'
    r'\(\s*_\(\s*"((?:[^"\\]|\\.)*)"\s*\)\s*\)|'
    r"_\(\s*'((?:[^'\\]|\\.)*)'\s*\)|"
    r"\(\s*_\(\s*'((?:[^'\\]|\\.)*)'\s*\)\s*\)"
    r')\s*:\s*(?:#.*)?$'
)


def _is_false_positive(text: str) -> bool:
    candidate = text.strip()
    if not candidate or len(candidate) < 2:
        return True
    if candidate.startswith(("[", "$", "#")):
        return True
    if "translate " in candidate.lower():
        return True
    if candidate.isupper() and len(candidate.split()) <= 2:
        return True
    if re.fullmatch(r"[-_./\\0-9]+", candidate):
        return True
    return False


def _normalize_context(context_stack: List[str], current_label: str | None) -> str:
    parts = []
    if current_label:
        parts.append(f"label:{current_label}")
    parts.extend(context_stack)
    return " > ".join(parts) if parts else "global"


def _iter_rpy_files(game_path: Path) -> Iterable[Path]:
    for file in sorted(game_path.rglob("*.rpy")):
        if "tl" in file.parts:
            continue
        yield file


def extract_translation_entries(game_path: str) -> List[TranslationEntry]:
    base_path = Path(game_path)
    entries: List[TranslationEntry] = []

    for file_path in _iter_rpy_files(base_path):
        current_label = None
        context_stack: List[str] = []
        context_indents: List[int] = []

        with file_path.open("r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                if line_number == 1:
                    line = line.lstrip("\ufeff")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                indent = len(line) - len(line.lstrip(" "))
                while context_indents and indent <= context_indents[-1]:
                    context_indents.pop()
                    context_stack.pop()

                label_match = LABEL_PATTERN.match(line)
                if label_match:
                    current_label = label_match.group(1)
                    context_stack = []
                    context_indents = []
                    continue

                block_match = BLOCK_PATTERN.match(line)
                if block_match:
                    block_name, block_tail = block_match.groups()
                    block_desc = block_tail.strip() or "block"
                    context_stack.append(f"{block_name}:{block_desc}")
                    context_indents.append(indent)
                    continue

                match = DIALOGUE_PATTERN.match(line)
                entry_type = "dialogue"
                extracted = None
                speaker = None
                if match:
                    speaker, t1, t2, t3, t4, t5, t6 = match.groups()
                    extracted = next(
                        (item for item in (t1, t2, t3, t4, t5, t6) if item is not None),
                        None,
                    )
                else:
                    menu_match = MENU_CHOICE_PATTERN.match(line)
                    if menu_match:
                        m1, m2, m3, m4, m5 = menu_match.groups()
                        extracted = next(
                            (item for item in (m1, m2, m3, m4, m5) if item is not None),
                            None,
                        )
                        entry_type = "menu_choice"
                    else:
                        narrator_match = NARRATOR_PATTERN.match(line)
                        if narrator_match:
                            t1, t2, t3, t4, t5, t6 = narrator_match.groups()
                            extracted = next(
                                (item for item in (t1, t2, t3, t4, t5, t6) if item is not None),
                                None,
                            )
                            entry_type = "narration"

                if extracted is None or _is_false_positive(extracted):
                    continue
                relative_path = str(file_path.relative_to(base_path)).replace("\\", "/")
                if current_label is None:
                    continue
                if entry_type == "dialogue" and speaker in SCREEN_LANGUAGE_KEYWORDS:
                    continue
                context_path = _normalize_context(context_stack, current_label)
                translation_id = build_translation_id(
                    original_text=extracted,
                    file_path=relative_path,
                    context_path=context_path,
                    entry_type=entry_type,
                )
                raw_code = line.strip()
                if "#" in raw_code:
                    raw_code = raw_code.split("#", 1)[0].rstrip()
                entries.append(
                    TranslationEntry(
                        original_text=extracted,
                        file_path=relative_path,
                        line_number=line_number,
                        entry_type=entry_type,
                        context_path=context_path,
                        translation_id=translation_id,
                        speaker=speaker,
                        raw_code=raw_code,
                    )
                )

    return entries


def save_entries(entries: List[TranslationEntry], output_path: str) -> Path:
    path = Path(output_path)
    path.write_text(
        json.dumps([entry.to_dict() for entry in entries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
