import json
import requests
from pathlib import Path
from syntax_guard import protect_placeholders, restore_placeholders

CACHE_FILE = Path("cache.json")
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

def translate_raw_text(text: str) -> str:
    payload = {
        "q": text,
        "source": "en",
        "target": "pt-BR",
        "format": "text"
    }
    response = requests.post(API_URL, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["translatedText"]

def translate_text(text, cache=None):
    if cache is None:
        cache = {}
    if text in cache:
        return cache[text]

    protected, placeholders = protect_placeholders(text)
    translated_protected = translate_raw_text(protected)
    translated = restore_placeholders(translated_protected, placeholders)

    cache[text] = translated
    return translated
