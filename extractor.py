import re
from pathlib import Path

from langdetect import detect, LangDetectException

# regex para pegar strings entre aspas simples ou duplas
STRING_PATTERN = re.compile(r'["\']([^"\']+)["\']')

# cache para não detectar idioma repetido
_lang_cache = {}


def looks_english_fast(text: str) -> bool:
    """
    Filtro ultra-rápido:
    elimina japonês, chinês, emojis, etc.
    """
    for ch in text:
        if ord(ch) > 0x3000:
            return False
    return True


def is_english(text: str) -> bool:
    """
    Detecta se é inglês com cache
    """
    if text in _lang_cache:
        return _lang_cache[text]

    try:
        result = detect(text) == "en"
    except LangDetectException:
        result = False

    _lang_cache[text] = result
    return result


def is_valid_string(text: str) -> bool:
    text = text.strip()

    # muito curto ou vazio
    if len(text) < 3:
        return False

    # ignora código / lixo técnico
    if text.startswith(("{", "[", "$", "#")):
        return False

    # ignora linhas de tradução
    if "translate " in text.lower():
        return False

    # frases muito curtas: assume inglês (ganho enorme de performance)
    if len(text.split()) < 3:
        return True

    # filtro rápido de unicode
    if not looks_english_fast(text):
        return False

    # detecção real (com cache)
    return is_english(text)


def extract_strings_from_file(path: Path):
    results = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                # ignora blocos de tradução
                if line.lstrip().startswith("translate "):
                    continue

                matches = STRING_PATTERN.findall(line)
                for m in matches:
                    if is_valid_string(m):
                        results.append(m)
    except Exception as e:
        print(f"Erro ao ler {path}: {e}")

    return results


def extract_from_folder(folder: str):
    all_strings = set()
    folder_path = Path(folder)

    for file in folder_path.rglob("*.rpy"):
        all_strings.update(extract_strings_from_file(file))

    return sorted(all_strings)
