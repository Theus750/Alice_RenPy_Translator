import json
import requests
from pathlib import Path
from syntax_guard import protect_placeholders, restore_placeholders

CACHE_FILE = Path("cache.json")
API_URL = "http://localhost:5000/translate"  # LibreTranslate local

def load_cache(cache_path: str | Path = CACHE_FILE):
    path = Path(cache_path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def save_cache(cache, cache_path: str | Path = CACHE_FILE):
    path = Path(cache_path)
    path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def translate_raw_text(text: str, source: str = "en", target: str = "pt-BR", api_url: str = API_URL) -> str:
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }
    response = requests.post(api_url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["translatedText"]

def translate_text(text, cache=None, source: str = "en", target: str = "pt-BR", api_url: str = API_URL):
    if cache is None:
        cache = {}
    if text in cache:
        return cache[text]

    protected, placeholders = protect_placeholders(text)
    translated_protected = translate_raw_text(protected, source=source, target=target, api_url=api_url)
    translated = restore_placeholders(translated_protected, placeholders)

    cache[text] = translated
    return translated
