import re
from typing import List, Tuple


PLACEHOLDER_PATTERN = re.compile(
    r"(\[[^\]]+\]|\{[^{}\n]+\}|%\([^)]+\)[a-zA-Z]|%[sd])"
)


def protect_placeholders(text: str) -> Tuple[str, List[str]]:
    placeholders = PLACEHOLDER_PATTERN.findall(text)
    protected = text
    for index, placeholder in enumerate(placeholders):
        protected = protected.replace(placeholder, f"__PH_{index}__", 1)
    return protected, placeholders


def restore_placeholders(text: str, placeholders: List[str]) -> str:
    restored = text
    for index, placeholder in enumerate(placeholders):
        restored = restored.replace(f"__PH_{index}__", placeholder)
    return restored
