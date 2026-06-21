from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .dialogue_output import save_dialogue_rpy, save_language_rpy, save_strings_rpy
from .syntax_guard import protect_placeholders, restore_placeholders
from .text_source_parser import extract_translation_entries, save_entries
from .translation_entry import TranslationEntry


logger = logging.getLogger(__name__)


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
    ) -> PipelineResult:
        logger.info("Validando projeto em %s", self.input_path)
        self._validate()
        logger.info("Lendo textos traduzíveis em %s", self.game_path)
        entries = extract_translation_entries(str(self.game_path))
        logger.info("%d entradas encontradas", len(entries))

        if cache is None:
            cache = {}

        translations: Dict[str, str] = {}
        if translator is not None:
            total_entries = len(entries)
            logger.info("Iniciando tradução de %d entradas", total_entries)
            for index, entry in enumerate(entries, start=1):
                if entry.original_text in cache:
                    translated = cache[entry.original_text]
                    logger.info("[%d/%d] cache hit: %s", index, total_entries, entry.original_text)
                else:
                    logger.info("[%d/%d] traduzindo: %s", index, total_entries, entry.original_text)
                    protected, placeholders = protect_placeholders(entry.original_text)
                    translated_protected = translator(protected)
                    translated = restore_placeholders(translated_protected, placeholders)
                    cache[entry.original_text] = translated
                translations[entry.translation_id] = translated
            logger.info("Tradução concluída para %d entradas", total_entries)

        logger.info("Salvando extração em %s", self.output_path)
        output_file = save_entries(entries, str(self.output_path))
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
                    else self.game_path / "zzz_renlocalizer_language.rpy"
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

    def _validate(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Projeto não encontrado: {self.input_path}")
        if not self.input_path.is_dir():
            raise NotADirectoryError(f"Caminho inválido (não é pasta): {self.input_path}")

        if not self.game_path.exists():
            raise FileNotFoundError(f"Pasta game não encontrada: {self.game_path}")
        if not self.game_path.is_dir():
            raise NotADirectoryError(f"Caminho inválido (não é pasta): {self.game_path}")

    @staticmethod
    def _resolve_paths(input_path: Path) -> tuple[Path, Path]:
        if input_path.name.lower() == "game":
            return input_path.parent, input_path

        if (input_path / "game").exists():
            return input_path, input_path / "game"

        return input_path, input_path / "game"
