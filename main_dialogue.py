from translation_pipeline import TranslationPipeline
from translator import load_cache, save_cache, translate_raw_text


def main() -> None:
    game_path = r"c:\Users\mathe\OneDrive\Área de Trabalho\jogo_teste\Beachfront-0.4-pc\game"
    cache = load_cache()

    pipeline = TranslationPipeline(
        project_path=game_path,
        output_path="extracted_entries.json",
    )
    result = pipeline.run(
        translator=translate_raw_text,
        cache=cache,
        language="portuguese",
        dialogue_output_path="game/tl/portuguese/dialogue.rpy",
        strings_output_path="game/tl/portuguese/strings.rpy",
    )
    save_cache(cache)

    print(f"Pipeline finalizado em {result.stage.value}")
    print(f"Entradas extraídas: {len(result.entries)}")
    print(f"Saída salva em: {result.output_file}")
    if result.dialogue_file:
        print(f"dialogue.rpy salvo em: {result.dialogue_file}")
    if result.strings_file:
        print(f"strings.rpy salvo em: {result.strings_file}")


if __name__ == "__main__":
    main()
