import json
import re
import requests
from pathlib import Path

CACHE_FILE = Path("cache.json")

VAR_PATTERN = re.compile(r'(\[[^\]]+\]|\{[^}]+\})')

API_URL = "https://api.mymemory.translated.net/get"


def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache):
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def protect_variables(text):
    variables = VAR_PATTERN.findall(text)
    protected = text

    for i, var in enumerate(variables):
        protected = protected.replace(var, f"__VAR{i}__")

    return protected, variables


def restore_variables(text, variables):
    restored = text
    for i, var in enumerate(variables):
        restored = restored.replace(f"__VAR{i}__", var)
    return restored


def translate_text(text, source="en", target="pt", cache=None):
    if cache is None:
        cache = {}

    if text in cache:
        return cache[text]

    protected, variables = protect_variables(text)

    protected = protected.replace("\n", " ").strip()


    params = {
        "q": protected,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()

    translated = response.json()["responseData"]["translatedText"]
    translated = restore_variables(translated, variables)

    cache[text] = translated
    return translated
