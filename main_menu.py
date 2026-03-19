from text_source_parser import extract_translation_entries
from dialogue_output import save_strings_rpy
from translator import load_cache, save_cache, translate_raw_text


def main() -> None:
    game_path = r"c:\Users\mathe\OneDrive\Área de Trabalho\jogo_teste\Beachfront-0.4-pc\game"
    cache = load_cache()

    entries = [
        entry
        for entry in extract_translation_entries(game_path)
        if entry.entry_type == "menu_choice"
    ]

    translations = {}
    for entry in entries:
        if entry.original_text in cache:
            translated = cache[entry.original_text]
        else:
            translated = translate_raw_text(entry.original_text)
            cache[entry.original_text] = translated
        translations[entry.translation_id] = translated

    output_file = save_strings_rpy(
        entries=entries,
        translations_by_id=translations,
        language="portuguese",
        output_path="game/tl/portuguese/menu.rpy",
    )
    save_cache(cache)

    print(f"Menus extraidos: {len(entries)}")
    print(f"menu.rpy salvo em: {output_file}")


if __name__ == "__main__":
    main()
