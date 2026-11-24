from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


_OLD_PATTERN = re.compile(r'^\s*old\s+"((?:[^"\\]|\\.)*)"\s*$')
_NEW_PATTERN = re.compile(r'^\s*new\s+"((?:[^"\\]|\\.)*)"\s*$')


@dataclass(frozen=True)
class TranslationBlock:
    old_text: str
    new_text: str
    file_path: Path
    line_number: int

    @property
    def is_pending(self) -> bool:
        return not self.new_text


def _decode_string(value: str) -> str:
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return value.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')


def parse_tl_file(file_path: str | Path) -> list[TranslationBlock]:
    path = Path(file_path)
    blocks: list[TranslationBlock] = []
    pending_old: tuple[str, int] | None = None

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        old_match = _OLD_PATTERN.match(line)
        if old_match:
            pending_old = (_decode_string(old_match.group(1)), line_number)
            continue

        new_match = _NEW_PATTERN.match(line)
        if new_match and pending_old is not None:
            old_text, old_line_number = pending_old
            blocks.append(
                TranslationBlock(
                    old_text=old_text,
                    new_text=_decode_string(new_match.group(1)),
                    file_path=path,
                    line_number=old_line_number,
                )
            )
            pending_old = None

    return blocks


def parse_tl_directory(directory_path: str | Path) -> list[TranslationBlock]:
    directory = Path(directory_path)
    blocks: list[TranslationBlock] = []
    for file_path in sorted(directory.rglob("*.rpy")):
        blocks.extend(parse_tl_file(file_path))
    return blocks


def pending_translation_blocks(directory_path: str | Path) -> list[TranslationBlock]:
    return [block for block in parse_tl_directory(directory_path) if block.is_pending]
