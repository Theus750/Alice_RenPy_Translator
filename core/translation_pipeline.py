from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .dialogue_output import save_dialogue_rpy, save_language_rpy, save_strings_rpy
from .syntax_guard import (
    TOKEN_TEMPLATE,
    placeholder_spacing_matches,
    placeholders_match,
    protect_placeholders,
    restore_placeholder_spacing,
    restore_placeholders,
)
from .text_source_parser import extract_translation_entries, find_named_menus, save_entries
from .translation_entry import TranslationEntry
from .rpa_adapter import RPAAdapter


logger = logging.getLogger(__name__)


def _normalize_translation(original_text: str, translated_text: str) -> str:
    if (
        translated_text.rstrip().endswith('"')
        and not original_text.rstrip().endswith('"')
        and translated_text.rstrip().count('"') % 2 == 1
    ):
        return translated_text.rstrip()[:-1].rstrip()
    return translated_text


def _is_untranslated_cache_value(original_text: str, translated_text: str) -> bool:
    """Identifica um cache hit que na prática não produziu tradução."""
    return (
        original_text.strip() == translated_text.strip()
        and any(character.isalpha() for character in original_text)
        and len(original_text.strip()) > 3
    )


def _translate_placeholder_segments(
    protected_text: str,
    placeholders: List[str],
    translator: Callable[[str], str],
) -> str:
    segments = [protected_text]
    for placeholder_index in range(len(placeholders)):
        token = TOKEN_TEMPLATE.format(index=placeholder_index)
        next_segments = []
        for segment in segments:
            next_segments.extend(segment.split(token))
        segments = next_segments

    translated_segments = [
        translator(segment) if segment else "" for segment in segments
    ]
    rebuilt = translated_segments[0]
    for placeholder_index, placeholder in enumerate(placeholders):
        rebuilt += placeholder
        rebuilt += translated_segments[placeholder_index + 1]
    return rebuilt


class PipelineStage(str, Enum):
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    TRANSLATING = "TRANSLATING"
    SAVING = "SAVING"


@dataclass
class PipelineResult:
    stage: PipelineStage
    entries: List[TranslationEntry]
    output_file: Optional[Path] = None
    translations: Optional[Dict[str, str]] = None
    dialogue_file: Optional[Path] = None
    strings_file: Optional[Path] = None
    language_file: Optional[Path] = None


class TranslationPipeline:
    def __init__(self, project_path: str, output_path: str = "extracted_entries.json"):
        self.input_path = Path(project_path)
        self.project_root, self.game_path = self._resolve_paths(self.input_path)
        self.output_path = Path(output_path) if output_path else self.project_root / "extracted_entries.json"

    def run(
        self,
        translator: Optional[Callable[[str], str]] = None,
        cache: Optional[Dict[str, str]] = None,
        language: str = "portuguese",
        dialogue_output_path: Optional[str] = None,
        strings_output_path: Optional[str] = None,
        language_output_path: Optional[str] = None,
        generate_language_file: bool = True,
        progress_callback: Optional[Callable[[str, int, int, str], None]] = None,
        batch_size: int = 200,
        batch_translator: Optional[Callable[[List[str]], List[str]]] = None,
        cache_checkpoint_size: int = 1000,
        cache_save_callback: Optional[Callable[[], None]] = None,
        glossary: Optional[Dict[str, str]] = None,
    ) -> PipelineResult:
        def progress(stage: str, current: int, total: int, message: str) -> None:
            if progress_callback:
                progress_callback(stage, current, total, message)

        logger.info("Validando projeto em %s", self.input_path)
        progress("VALIDATING", 0, 1, "Validando projeto")
        self._extract_rpa_archives()
        self._validate()
        logger.info("Lendo textos traduzíveis em %s", self.game_path)
        named_menus = find_named_menus(str(self.game_path))
        if named_menus:
            logger.info(
                "%d menus nomeados detectados: %s",
                len(named_menus),
                ", ".join(menu.name for menu in named_menus),
            )
        entries = extract_translation_entries(str(self.game_path))
        logger.info("%d entradas encontradas", len(entries))
        progress("PARSING", len(entries), len(entries), f"{len(entries)} entradas encontradas")

        if cache is None:
            cache = {}

        translations: Dict[str, str] = {}
        glossary = glossary or {}
        if translator is not None:
            total_entries = len(entries)
            batch_size = max(1, batch_size)
            cache_checkpoint_size = max(1, cache_checkpoint_size)
            logger.info("Iniciando tradução de %d entradas", total_entries)
            for batch_start in range(0, total_entries, batch_size):
                batch = entries[batch_start:batch_start + batch_size]
                pending = []
                pending_meta = []
                for entry in batch:
                    if entry.entry_type in {"menu_choice", "menu_caption", "screen_string", "python_string", "input_string"} and entry.original_text in glossary:
                        translated = glossary[entry.original_text]
                        cache[entry.original_text] = translated
                        translations[entry.translation_id] = translated
                    elif (
                        entry.original_text in cache
                        and not _is_untranslated_cache_value(
                            entry.original_text,
                            cache[entry.original_text],
                        )
                        and placeholders_match(
                            entry.original_text,
                            cache[entry.original_text],
                        )
                        and placeholder_spacing_matches(
                            entry.original_text,
                            cache[entry.original_text],
                        )
                    ):
                        translations[entry.translation_id] = cache[entry.original_text]
                    else:
                        protected, placeholders = protect_placeholders(entry.original_text)
                        if placeholders:
                            translated = _translate_placeholder_segments(
                                protected,
                                placeholders,
                                translator,
                            )
                            translated = restore_placeholders(translated, placeholders)
                            translated = restore_placeholder_spacing(
                                entry.original_text,
                                translated,
                            )
                            if not placeholders_match(
                                entry.original_text,
                                translated,
                            ) or not placeholder_spacing_matches(
                                entry.original_text,
                                translated,
                            ):
                                logger.warning(
                                    "Tradução de placeholders inválida; usando texto original: %s:%d",
                                    entry.file_path,
                                    entry.line_number,
                                )
                                translated = entry.original_text
                            cache[entry.original_text] = translated
                            translations[entry.translation_id] = translated
                        else:
                            pending.append(protected)
                            pending_meta.append((entry, placeholders, protected))
                logger.info("traduzindo: lote %d-%d/%d", batch_start + 1, index if 'index' in locals() else min(batch_start + len(batch), total_entries), total_entries)
                if batch_translator and pending:
                    try:
                        results = batch_translator(pending)
                    except Exception as error:
                        logger.warning("Batch indisponível (%s); usando tradução individual", error)
                        results = [translator(text) for text in pending]
                else:
                    results = [translator(text) for text in pending]
                if len(results) != len(pending_meta):
                    raise ValueError(
                        "O motor retornou uma quantidade de traduções diferente "
                        "da quantidade de entradas enviadas"
                    )
                for (entry, placeholders, protected), translated_protected in zip(
                    pending_meta, results
                ):
                    if placeholders:
                        # Tokens artificiais são alterados pelo LibreTranslate.
                        # Traduzir os segmentos evita que o motor modifique
                        # placeholders Ren'Py.
                        translated = _translate_placeholder_segments(
                            protected,
                            placeholders,
                            translator,
                        )
                    else:
                        translated = translated_protected
                    translated = restore_placeholders(translated, placeholders)
                    translated = restore_placeholder_spacing(entry.original_text, translated)
                    if not placeholders_match(entry.original_text, translated):
                        # Alguns motores removem tokens do texto traduzido.
                        # Nesse caso, traduzimos cada trecho separado e
                        # remontamos a frase preservando as variáveis Ren'Py.
                        logger.warning(
                            "Placeholder removido pelo motor; traduzindo trechos separados: %s:%d",
                            entry.file_path,
                            entry.line_number,
                        )
                        translated = _translate_placeholder_segments(
                            protected,
                            placeholders,
                            translator,
                        )
                        if not placeholders_match(entry.original_text, translated):
                            logger.warning(
                                "Não foi possível preservar placeholders; usando texto original: %s:%d",
                                entry.file_path,
                                entry.line_number,
                            )
                            translated = entry.original_text
                    translated = restore_placeholder_spacing(
                        entry.original_text,
                        translated,
                    )
                    if not placeholder_spacing_matches(
                        entry.original_text,
                        translated,
                    ):
                        logger.warning(
                            "Espaçamento de placeholder inválido; usando texto original: %s:%d",
                            entry.file_path,
                            entry.line_number,
                        )
                        translated = entry.original_text
                    translated = _normalize_translation(entry.original_text, translated)
                    cache[entry.original_text] = translated
                    translations[entry.translation_id] = translated
                index = min(batch_start + len(batch), total_entries)
                progress("TRANSLATING", index - 1, len(entries), f"Traduzindo entrada {index}/{len(entries)}")
                if index % batch_size == 0 or index == total_entries:
                    logger.info("Batch concluido: %d/%d entradas", index, total_entries)
                    progress("TRANSLATING", index, total_entries, f"Batch concluido: {index}/{total_entries}")
                if cache_save_callback and (index % cache_checkpoint_size == 0 or index == total_entries):
                    cache_save_callback()
                    logger.info("Checkpoint do cache salvo: %d/%d entradas", index, total_entries)
            logger.info("Tradução concluída para %d entradas", total_entries)

        logger.info("Salvando extração em %s", self.output_path)
        output_file = save_entries(entries, str(self.output_path))
        progress("SAVING", 1, 1, "Salvando arquivos gerados")
        dialogue_file = None
        strings_file = None
        language_file = None
        if translator is not None:
            output_dir = self.game_path / "tl" / language
            dialogue_path = Path(dialogue_output_path) if dialogue_output_path else output_dir / "dialogue.rpy"
            strings_path = Path(strings_output_path) if strings_output_path else output_dir / "strings.rpy"
            logger.info("Gerando arquivos Ren'Py em %s", output_dir)
            dialogue_file = save_dialogue_rpy(
                entries=entries,
                translations_by_id=translations,
                language=language,
                output_path=str(dialogue_path),
            )
            strings_file = save_strings_rpy(
                entries=entries,
                translations_by_id=translations,
                language=language,
                output_path=str(strings_path),
            )
            if generate_language_file:
                language_path = (
                    Path(language_output_path)
                    if language_output_path
                    else self.game_path / "zzz_alice_language.rpy"
                )
                logger.info("Gerando arquivo de idioma em %s", language_path)
                language_file = save_language_rpy(language=language, output_path=str(language_path))
            else:
                logger.info("Geração de arquivo de idioma desativada")
            logger.info("Arquivos gerados: %s, %s, %s", dialogue_file, strings_file, language_file)

        return PipelineResult(
            stage=PipelineStage.SAVING,
            entries=entries,
            output_file=output_file,
            translations=translations or None,
            dialogue_file=dialogue_file,
            strings_file=strings_file,
            language_file=language_file,
        )

    def _extract_rpa_archives(self) -> None:
        adapter = RPAAdapter()
        success, total, extracted = adapter.extract_game(self.game_path)
        if total:
            logger.info("RPA: %d/%d arquivo(s) extraído(s)", extracted, total)
        if not success:
            raise RuntimeError(f"não foi possível extrair todos os arquivos RPA ({extracted}/{total})")

    def _validate(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Projeto não encontrado: {self.input_path}")
        if not self.input_path.is_dir():
            raise NotADirectoryError(f"Caminho inválido (não é pasta): {self.input_path}")

        if not self.game_path.exists():
            raise FileNotFoundError(f"Pasta game não encontrada: {self.game_path}")
        if not self.game_path.is_dir():
            raise NotADirectoryError(f"Caminho inválido (não é pasta): {self.game_path}")

        source_files = [
            path
            for path in self.game_path.rglob("*.rpy")
            if "tl" not in path.relative_to(self.game_path).parts
        ]
        compiled_files = [
            path
            for pattern in ("*.rpyc", "*.rpymc")
            for path in self.game_path.rglob(pattern)
            if "tl" not in path.relative_to(self.game_path).parts
        ]
        if not source_files and not compiled_files:
            raise FileNotFoundError(
                f"Nenhum arquivo .rpy, .rpyc ou .rpymc encontrado em: {self.game_path}"
            )

    @staticmethod
    def _resolve_paths(input_path: Path) -> tuple[Path, Path]:
        if input_path.name.lower() == "game":
            return input_path.parent, input_path

        if (input_path / "game").exists():
            return input_path, input_path / "game"

        return input_path, input_path / "game"
