"""RPA extraction with optional unrpa support and a native fallback."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from .rpa_parser import RPAParser


class RPAAdapter:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def find_archives(game_path: Path) -> list[Path]:
        return sorted(
            path for path in game_path.rglob("*")
            if path.is_file() and path.suffix.lower() == ".rpa"
        )

    def extract_archive(self, archive: Path, output_dir: Path) -> bool:
        try:
            from unrpa import UnRPA
        except ImportError:
            return RPAParser().extract_archive(archive, output_dir)

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            original_cwd = os.getcwd()
            try:
                os.chdir(output_dir)
                UnRPA(str(archive), verbosity=0).extract_files()
            finally:
                os.chdir(original_cwd)
            return True
        except Exception as error:
            self.logger.warning("unrpa falhou para %s; usando parser nativo: %s", archive, error)
            return RPAParser().extract_archive(archive, output_dir)

    def extract_game(self, game_path: Path) -> tuple[bool, int, int]:
        archives = self.find_archives(game_path)
        if not archives:
            return True, 0, 0
        successful = sum(
            self.extract_archive(archive, archive.parent)
            for archive in archives
        )
        return successful == len(archives), len(archives), successful
