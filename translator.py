"""Compatibility exports for the consolidated core translator module."""

from core.translator import (
    API_URL,
    CACHE_FILE,
    load_cache,
    save_cache,
    translate_raw_text,
    translate_text,
)

__all__ = [
    "API_URL",
    "CACHE_FILE",
    "load_cache",
    "save_cache",
    "translate_raw_text",
    "translate_text",
]
