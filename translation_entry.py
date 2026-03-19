from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1


@dataclass(frozen=True)
class TranslationEntry:
    original_text: str
    file_path: str
    line_number: int
    entry_type: str
    context_path: str
    translation_id: str
    speaker: str | None = None
    raw_code: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def build_translation_id(
    *,
    original_text: str,
    file_path: str,
    context_path: str,
    entry_type: str,
) -> str:
    source = "||".join(
        [
            original_text.strip(),
            file_path.replace("\\", "/"),
            context_path.strip(),
            entry_type.strip(),
        ]
    )
    return sha1(source.encode("utf-8")).hexdigest()[:16]
