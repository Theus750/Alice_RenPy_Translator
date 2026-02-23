from extractor_dialogue import extract_dialogues
from translator import translate_text, load_cache, save_cache
from generator_dialogue import generate_dialogue_rpy

def main():
    game_path = r"c:\Users\mathe\OneDrive\Área de Trabalho\jogo_teste\Beachfront-0.4-pc\game"

    dialogues = extract_dialogues(game_path)

    cache = load_cache()

    for label, items in dialogues.items():
        for who, text in items:
            if text not in cache:
                print(f"Traduzindo: {text}")
                translate_text(text, cache)

    save_cache(cache)
    generate_dialogue_rpy(dialogues, cache)

    print("🎯 Diálogos traduzidos com sucesso")

if __name__ == "__main__":
    main()
