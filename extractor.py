import re
import unicodedata
from pathlib import Path

# Regex seguro para Ren'Py
STRING_PATTERN = re.compile(
    r'"([^"]+)"|\'([^\']+)\''
)


def normalize_text(text: str) -> str:
    """
    Normaliza unicode (’ … → consistentes)
    """
    return unicodedata.normalize("NFKC", text)


def looks_like_code(text: str) -> bool:
    """
    Heurística simples para ignorar código/lixo
    """
    return text.startswith(("{", "[", "$", "#"))


def is_valid_string(text: str) -> bool:
    text = normalize_text(text.strip())

    # vazio ou muito curto
    if len(text) < 3:
        return False

    # ignora código
    if looks_like_code(text):
        return False

    # ignora traduções existentes
    if "translate " in text.lower():
        return False

    # ignora linhas muito técnicas
    if text.isupper() and len(text.split()) <= 2:
        return False

    return True


def extract_strings_from_file(path: Path):
    results = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.lstrip()

                # ignora blocos de tradução
                if stripped.startswith("translate "):
                    continue

                matches = STRING_PATTERN.findall(line)

                for g1, g2 in matches:
                    text = g1 or g2
                    text = normalize_text(text)

                    if is_valid_string(text):
                        results.append(text)

    except Exception as e:
        print(f"Erro ao ler {path}: {e}")

    return results


def extract_from_folder(folder: str):
    all_strings = []
    seen = set()

    folder_path = Path(folder)

    for file in folder_path.rglob("*.rpy"):
        for text in extract_strings_from_file(file):
            if text not in seen:
                seen.add(text)
                all_strings.append(text)

    return all_strings
