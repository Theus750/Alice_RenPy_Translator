import re
from typing import List, Tuple


PLACEHOLDER_PATTERN = re.compile(
    r"(\\[nrt]|\[[^\]]+\]|\{[^{}\n]+\}|%\([^)]+\)[a-zA-Z]|%[sd])"
)
TOKEN_TEMPLATE = "[[[PH_{index}]]]"


def protect_placeholders(text: str) -> Tuple[str, List[str]]:
    placeholders = PLACEHOLDER_PATTERN.findall(text)
    protected = text
    for index, placeholder in enumerate(placeholders):
        protected = protected.replace(placeholder, TOKEN_TEMPLATE.format(index=index), 1)
    return protected, placeholders


def restore_placeholders(text: str, placeholders: List[str]) -> str:
    restored = text
    for index, placeholder in enumerate(placeholders):
        variants = [
            TOKEN_TEMPLATE.format(index=index),
            f"[[PH_{index}]]",
            f"[[[PH_{index}]]",
            f"[[PH_{index}]]]",
            f"[PH_{index}]",
            f"__PH_{index}__",
            f"__PH_{index}_",
            f"__VAR{index}_",
            f"__VAR_{index}__",
            f"PH_{index}",
        ]
        for token in variants:
            restored = restored.replace(token, placeholder)
    return restored
