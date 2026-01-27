import json
import re
import requests
from pathlib import Path

CACHE_FILE = Path("cache.json")
VAR_PATTERN = re.compile(r'(\[[^\]]+\]|\{[^}]+\})')
API_URL = "http://localhost:5000/translate"  # LibreTranslate local

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

def translate_text(text, cache=None):
    if cache is None:
        cache = {}
    if text in cache:
        return cache[text]

    protected, variables = protect_variables(text)
    payload = {
        "q": protected,
        "source": "en",
        "target": "pt-BR",
        "format": "text"
    }
    r = requests.post(API_URL, json=payload, timeout=60)  # <- importante trocar data -> json

    r.raise_for_status()
    translated = r.json()["translatedText"]
    translated = restore_variables(translated, variables)

    cache[text] = translated
    return translated
