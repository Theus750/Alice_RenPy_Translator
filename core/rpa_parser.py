"""Safe native extraction for Ren'Py RPA-2.0 and RPA-3.0 archives."""

from __future__ import annotations

import io
import logging
import pickle
import posixpath
import zlib
from pathlib import Path
from typing import BinaryIO


class _RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module: str, name: str):
        if module == "builtins" and name in {"bytes", "bytearray", "dict", "int", "list", "set", "str", "tuple"}:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(f"global não permitido no índice RPA: {module}.{name}")


def _safe_loads(data: bytes):
    try:
        payload = zlib.decompress(data)
    except zlib.error:
        payload = data
    return _RestrictedUnpickler(io.BytesIO(payload)).load()


def _safe_relative_path(name: object) -> Path | None:
    if isinstance(name, bytes):
        name = name.decode("utf-8", errors="strict")
    if not isinstance(name, str) or not name:
        return None
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or ":" in normalized.split("/", 1)[0]:
        return None
    parts = [part for part in posixpath.normpath(normalized).split("/") if part not in {"", "."}]
    if not parts or any(part == ".." for part in parts):
        return None
    return Path(*parts)


class RPAParser:
    """Extract RPA archives without executing objects stored in their index."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def extract_archive(self, rpa_path: Path, output_dir: Path) -> bool:
        if not rpa_path.is_file():
            self.logger.error("Arquivo RPA não encontrado: %s", rpa_path)
            return False
        try:
            with rpa_path.open("rb") as archive:
                header = archive.readline()
                if header.startswith(b"RPA-3.0"):
                    index_offset, key = self._parse_header(header, 3)
                elif header.startswith(b"RPA-2.0"):
                    index_offset, key = self._parse_header(header, 2)
                else:
                    self.logger.error("Formato RPA desconhecido: %s", header[:20])
                    return False
                archive.seek(index_offset)
                index = _safe_loads(archive.read())
                return self._extract_files(archive, index, output_dir, key)
        except (OSError, EOFError, ValueError, TypeError, pickle.PickleError, zlib.error) as error:
            self.logger.error("Falha ao extrair %s: %s", rpa_path, error)
            return False

    @staticmethod
    def _parse_header(header: bytes, version: int) -> tuple[int, int]:
        parts = header.decode("ascii").strip().split()
        required = 3 if version == 3 else 2
        if len(parts) < required:
            raise ValueError("cabeçalho RPA incompleto")
        offset = int(parts[1], 16)
        key = int(parts[2], 16) if version == 3 else 0
        if offset < 0 or key < 0:
            raise ValueError("cabeçalho RPA inválido")
        return offset, key

    def _extract_files(
        self,
        archive: BinaryIO,
        index: object,
        output_dir: Path,
        key: int,
    ) -> bool:
        if not isinstance(index, dict):
            raise ValueError("índice RPA inválido")
        output_dir.mkdir(parents=True, exist_ok=True)
        extracted = 0
        archive_size = self._archive_size(archive)
        for filename, records in index.items():
            relative_path = _safe_relative_path(filename)
            if relative_path is None or not isinstance(records, (list, tuple)) or not records:
                continue
            record = records[0]
            if not isinstance(record, (list, tuple)) or len(record) < 2:
                continue
            try:
                offset = int(record[0]) ^ key
                length = int(record[1]) ^ key
                prefix = record[2] if len(record) > 2 else b""
                if isinstance(prefix, str):
                    prefix = prefix.encode("latin-1")
                if not isinstance(prefix, bytes) or offset < 0 or length < len(prefix) or offset + length > archive_size:
                    continue
                archive.seek(offset)
                content = prefix + archive.read(length - len(prefix))
                destination = output_dir / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
                extracted += 1
            except (OSError, TypeError, ValueError, OverflowError) as error:
                self.logger.warning("Entrada RPA ignorada (%s): %s", filename, error)
        self.logger.info("Extraídos %d arquivo(s) do RPA", extracted)
        return extracted > 0

    @staticmethod
    def _archive_size(archive: BinaryIO) -> int:
        current = archive.tell()
        archive.seek(0, 2)
        size = archive.tell()
        archive.seek(current)
        return size
