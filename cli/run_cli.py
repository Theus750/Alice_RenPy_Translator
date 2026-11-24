from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

from core.config_manager import ConfigManager
from core.translation_pipeline import TranslationPipeline
from core.translator import (
    load_cache,
    purge_invalid_placeholder_cache,
    save_cache,
    translate_raw_text,
    translate_raw_texts,
)


def _resolve_relative_path(base_path: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return base_path / path


def _infer_renpy_language(config) -> str:
    for candidate in (config.project.dialogue_output_path, config.project.strings_output_path):
        if not candidate:
            continue
        parent_name = Path(candidate).parent.name.strip()
        if parent_name:
            return parent_name.replace("-", "_")
    return "portuguese"


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Executa o pipeline de tradução Ren'Py via CLI")
    parser.add_argument("project_path", nargs="?", help="Caminho da pasta raiz do projeto ou da pasta game")
    parser.add_argument("--config", default="config.json", help="Caminho do arquivo de configuração")
    parser.add_argument("--show-config", action="store_true", help="Mostra a configuração atual e sai")
    parser.add_argument("--edit-config", action="store_true", help="Salva as opções fornecidas em config.json e sai")
    parser.add_argument("--set-project-path", help="Atualiza o caminho do projeto no config.json")
    parser.add_argument("--set-extracted-entries-path", help="Atualiza o caminho do extracted_entries.json no config.json")
    parser.add_argument("--set-cache-path", help="Atualiza o caminho do cache no config.json")
    parser.add_argument("--set-dialogue-output-path", help="Atualiza o caminho do dialogue.rpy no config.json")
    parser.add_argument("--set-strings-output-path", help="Atualiza o caminho do strings.rpy no config.json")
    parser.add_argument("--set-source-language", help="Atualiza o idioma de origem no config.json")
    parser.add_argument("--set-target-language", help="Atualiza o idioma de destino no config.json")
    parser.add_argument("--set-language", help="Atualiza o idioma da interface no config.json")
    parser.add_argument("--set-selected-engine", help="Atualiza o motor selecionado no config.json")
    parser.add_argument("--set-api-url", help="Atualiza o endpoint de tradução no config.json")
    parser.add_argument("--set-theme", help="Atualiza o tema da interface no config.json")
    parser.add_argument("--set-last-opened-project", help="Atualiza o último projeto aberto no config.json")
    parser.add_argument("--set-max-batch-size", type=int, help="Atualiza o batch size no config.json")
    parser.add_argument("--set-max-retries", type=int, help="Atualiza o número de retries no config.json")
    parser.add_argument("--set-timeout", type=int, help="Atualiza o timeout no config.json")
    parser.add_argument("--enable-runtime-hook", action="store_true", help="Ativa o runtime hook no config.json")
    parser.add_argument("--disable-runtime-hook", action="store_true", help="Desativa o runtime hook no config.json")
    parser.add_argument("--source-language", help="Idioma de origem para o tradutor")
    parser.add_argument("--target-language", help="Idioma de destino para o tradutor")
    parser.add_argument("--language", help="Nome da pasta tl de saída")
    parser.add_argument("--cache-path", help="Caminho do cache de traduções")
    parser.add_argument("--output-path", help="Caminho do arquivo extracted_entries.json")
    parser.add_argument("--dialogue-output", help="Caminho do arquivo dialogue.rpy")
    parser.add_argument("--strings-output", help="Caminho do arquivo strings.rpy")
    parser.add_argument("--language-output", help="Caminho do arquivo de ativação de idioma")
    parser.add_argument("--skip-language-file", action="store_true", help="Não gera o arquivo de ativação de idioma")
    return parser


def _apply_config_overrides(config, args) -> bool:
    changed = False

    if args.set_project_path is not None:
        config.project.project_path = args.set_project_path
        changed = True
    if args.set_extracted_entries_path is not None:
        config.project.extracted_entries_path = args.set_extracted_entries_path
        changed = True
    if args.set_cache_path is not None:
        config.project.cache_path = args.set_cache_path
        changed = True
    if args.set_dialogue_output_path is not None:
        config.project.dialogue_output_path = args.set_dialogue_output_path
        changed = True
    if args.set_strings_output_path is not None:
        config.project.strings_output_path = args.set_strings_output_path
        changed = True

    if args.set_source_language is not None:
        config.translation.source_language = args.set_source_language
        changed = True
    if args.set_target_language is not None:
        config.translation.target_language = args.set_target_language
        changed = True
    if args.set_selected_engine is not None:
        config.translation.selected_engine = args.set_selected_engine
        changed = True
    if args.set_api_url is not None:
        config.translation.api_url = args.set_api_url
        changed = True
    if args.set_max_batch_size is not None:
        config.translation.max_batch_size = args.set_max_batch_size
        changed = True
    if args.set_max_retries is not None:
        config.translation.max_retries = args.set_max_retries
        changed = True
    if args.set_timeout is not None:
        config.translation.timeout = args.set_timeout
        changed = True
    if args.enable_runtime_hook:
        config.translation.enable_runtime_hook = True
        changed = True
    if args.disable_runtime_hook:
        config.translation.enable_runtime_hook = False
        changed = True

    if args.set_language is not None:
        config.ui.locale = args.set_language
        changed = True

    if args.set_theme is not None:
        config.ui.theme = args.set_theme
        changed = True
    if args.set_last_opened_project is not None:
        config.ui.last_opened_project = args.set_last_opened_project
        changed = True

    return changed


def main() -> None:
    args = build_parser().parse_args()

    config_manager = ConfigManager(args.config)
    config = config_manager.load()

    if args.show_config:
        print(json.dumps(asdict(config), ensure_ascii=False, indent=2))
        return

    changed = _apply_config_overrides(config, args)
    if args.edit_config or changed:
        config_manager.save(config)
        print(f"Configuração salva em: {config_manager.config_path}")
        return

    _configure_logging()

    default_project_path = Path(__file__).resolve().parent.parent
    project_path = Path(args.project_path or config.project.project_path or default_project_path)
    project_pipeline = TranslationPipeline(project_path=str(project_path), output_path="")

    project_root = project_pipeline.project_root
    source_language = args.source_language or config.translation.source_language
    target_language = args.target_language or config.translation.target_language
    language = args.language or _infer_renpy_language(config)

    configured_cache = args.cache_path or config.project.cache_path
    if not args.cache_path and configured_cache == "cache.json":
        configured_cache = str(project_root / ".alice" / "cache.json")
    cache_path = _resolve_relative_path(config_manager.config_path.parent, configured_cache)
    invalid_cache_entries = purge_invalid_placeholder_cache(cache_path or config.project.cache_path)
    if invalid_cache_entries:
        print(
            f"Cache: {invalid_cache_entries} entradas inválidas removidas "
            "para retradução."
        )
    cache = load_cache(cache_path or config.project.cache_path)
    glossary = config_manager.load_glossary("menu_glossary.json")

    output_path = _resolve_relative_path(project_root, args.output_path or config.project.extracted_entries_path)
    dialogue_path = _resolve_relative_path(project_root, args.dialogue_output or config.project.dialogue_output_path)
    strings_path = _resolve_relative_path(project_root, args.strings_output or config.project.strings_output_path)
    language_path = None if args.skip_language_file else _resolve_relative_path(project_root, args.language_output)

    pipeline = TranslationPipeline(
        project_path=str(project_path),
        output_path=str(output_path) if output_path else "",
    )
    result = pipeline.run(
        translator=lambda text: translate_raw_text(text, source=source_language, target=target_language),
        cache=cache,
        language=language,
        dialogue_output_path=str(dialogue_path) if dialogue_path else None,
        strings_output_path=str(strings_path) if strings_path else None,
        language_output_path=str(language_path) if language_path else None,
        generate_language_file=not args.skip_language_file,
        batch_size=config.translation.max_batch_size,
        batch_translator=lambda texts: translate_raw_texts(texts, source=source_language, target=target_language, api_url=config.translation.api_url, max_retries=config.translation.max_retries, timeout=config.translation.timeout),
        cache_checkpoint_size=1000,
        cache_save_callback=lambda: save_cache(cache, cache_path or config.project.cache_path),
        glossary=glossary,
    )
    save_cache(cache, cache_path or config.project.cache_path)

    print(f"Pipeline finalizado em {result.stage.value}")
    print(f"Entradas extraídas: {len(result.entries)}")
    print(f"Saída salva em: {result.output_file}")
    if result.dialogue_file:
        print(f"dialogue.rpy salvo em: {result.dialogue_file}")
    if result.strings_file:
        print(f"strings.rpy salvo em: {result.strings_file}")
    if result.language_file:
        print(f"language.rpy salvo em: {result.language_file}")


if __name__ == "__main__":
    main()
