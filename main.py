from pathlib import Path

from extractor import extract_from_folder
from translator import translate_text, load_cache, save_cache
from generator import generate_strings_rpy


def main():
    game_path = r"c:\Users\mathe\OneDrive\Área de Trabalho\jogo_teste\Beachfront-0.4-pc\game"

    texts = extract_from_folder(game_path)
    total = len(texts)

    print(f"🔹 {total} textos encontrados")

    cache = load_cache()

    for i, text in enumerate(texts, start=1):
        if text in cache:
            continue

        print(f"[{i}/{total}] Traduzindo: {text}")
        translate_text(text, cache)

    save_cache(cache)

    # 👉 GERA O strings.rpy USANDO O generator.py
    generate_strings_rpy(cache)

    print(f"🎯 Tradução finalizada: {len(cache)}/{total}")


if __name__ == "__main__":
    main()
