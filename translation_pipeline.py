from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional

from dialogue_output import save_dialogue_rpy
from syntax_guard import protect_placeholders, restore_placeholders
from text_source_parser import extract_translation_entries, save_entries
from translation_entry import TranslationEntry


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


class TranslationPipeline:
    def __init__(self, project_path: str, output_path: str = "extracted_entries.json"):
        self.project_path = Path(project_path)
        self.output_path = output_path

    def run(
        self,
        translator: Optional[Callable[[str], str]] = None,
        cache: Optional[Dict[str, str]] = None,
        language: str = "portuguese",
        dialogue_output_path: str = "game/tl/portuguese/dialogue.rpy",
    ) -> PipelineResult:
        self._validate()
        entries = extract_translation_entries(str(self.project_path))

        if cache is None:
            cache = {}

        translations: Dict[str, str] = {}
        if translator is not None:
            for entry in entries:
                if entry.original_text in cache:
                    translated = cache[entry.original_text]
                else:
                    protected, placeholders = protect_placeholders(entry.original_text)
                    translated_protected = translator(protected)
                    translated = restore_placeholders(translated_protected, placeholders)
                    cache[entry.original_text] = translated
                translations[entry.translation_id] = translated

        output_file = save_entries(entries, self.output_path)
        dialogue_file = None
        if translator is not None:
            dialogue_file = save_dialogue_rpy(
                entries=entries,
                translations_by_id=translations,
                language=language,
                output_path=dialogue_output_path,
            )

        return PipelineResult(
            stage=PipelineStage.SAVING,
            entries=entries,
            output_file=output_file,
            translations=translations or None,
            dialogue_file=dialogue_file,
        )

    def _validate(self) -> None:
        if not self.project_path.exists():
            raise FileNotFoundError(f"Projeto não encontrado: {self.project_path}")
        if not self.project_path.is_dir():
            raise NotADirectoryError(f"Caminho inválido (não é pasta): {self.project_path}")
