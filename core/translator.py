import json
import requests
import time
from pathlib import Path
from .syntax_guard import (
    placeholder_spacing_matches,
    placeholders_match,
    protect_placeholders,
    restore_placeholders,
)

CACHE_FILE = Path("cache.json")
API_URL = "http://localhost:5000/translate"  # LibreTranslate local

def load_cache(cache_path: str | Path = CACHE_FILE):
    path = Path(cache_path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def save_cache(cache, cache_path: str | Path = CACHE_FILE):
    path = Path(cache_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def purge_invalid_placeholder_cache(cache_path: str | Path = CACHE_FILE) -> int:
    """Remove traduções inválidas ou iguais ao texto original."""
    path = Path(cache_path)
    cache = load_cache(path)
    invalid_keys = [
        original for original, translated in cache.items()
        if not placeholders_match(original, translated)
        or not placeholder_spacing_matches(original, translated)
        or (
            original.strip() == translated.strip()
            and len(original.strip()) > 3
            and any(character.isalpha() for character in original)
        )
    ]
    for original in invalid_keys:
        del cache[original]
    if invalid_keys:
        save_cache(cache, path)
    return len(invalid_keys)

def translate_raw_text(text: str, source: str = "en", target: str = "pt-BR", api_url: str = API_URL, timeout: int = 60) -> str:
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }
    response = requests.post(api_url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()["translatedText"]


def translate_raw_texts(texts: list[str], source: str = "en", target: str = "pt-BR", api_url: str = API_URL, max_retries: int = 3, timeout: int = 120) -> list[str]:
    if not texts:
        return []
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(api_url, json={"q": texts, "source": source, "target": target, "format": "text"}, timeout=timeout)
            response.raise_for_status()
            translated = response.json().get("translatedText")
            if isinstance(translated, list) and len(translated) == len(texts):
                return translated
            raise ValueError("O motor não retornou uma lista de traduções compatível")
        except (requests.RequestException, ValueError) as error:
            last_error = error
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Falha após {max_retries + 1} tentativas: {last_error}")

def translate_text(text, cache=None, source: str = "en", target: str = "pt-BR", api_url: str = API_URL):
    if cache is None:
        cache = {}
    if text in cache:
        return cache[text]

    protected, placeholders = protect_placeholders(text)
    translated_protected = translate_raw_text(protected, source=source, target=target, api_url=api_url)
    translated = restore_placeholders(translated_protected, placeholders)
    translated = restore_placeholder_spacing(text, translated)

    cache[text] = translated
    return translated
