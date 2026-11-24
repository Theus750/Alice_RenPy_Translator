"""Safe, dependency-free readers for Ren'Py compiled script caches.

The reader only deserializes data and never imports or executes Ren'Py code.
It supports the RPC2 container used by Ren'Py 8.5.2 and the older raw-zlib
variant.  Unrecognised Ren'Py classes are represented by inert containers.
"""

from __future__ import annotations

import io
import pickle
import struct
import zlib
from pathlib import Path
from typing import Any, Iterator

from .translation_entry import TranslationEntry, build_translation_id


class CompiledReadError(ValueError):
    """The compiled file is invalid or uses an unsupported container."""


class _InertRenpyObject:
    def __setstate__(self, state: Any) -> None:
        if isinstance(state, dict):
            self.__dict__.update(state)
        elif isinstance(state, tuple):
            for part in state:
                if isinstance(part, dict):
                    self.__dict__.update(part)


class SafeRenpyUnpickler(pickle.Unpickler):
    """Allow data types required by Ren'Py while rejecting callable globals."""

    _safe_builtins = {
        "bool": bool, "bytes": bytes, "bytearray": bytearray, "dict": dict,
        "float": float, "frozenset": frozenset, "int": int, "list": list,
        "set": set, "str": str, "tuple": tuple,
    }

    def find_class(self, module: str, name: str) -> type:
        if module == "builtins" and name in self._safe_builtins:
            return self._safe_builtins[name]
        if module == "collections" and name in {"defaultdict", "OrderedDict"}:
            from collections import OrderedDict, defaultdict
            return {"defaultdict": defaultdict, "OrderedDict": OrderedDict}[name]
        if module.startswith(("renpy.", "store")):
            return type(f"RenPy_{name}", (_InertRenpyObject,), {"__module__": module})
        raise pickle.UnpicklingError(f"global bloqueado: {module}.{name}")


def _rpc2_payloads(raw: bytes) -> list[bytes]:
    if not raw.startswith(b"RENPY RPC") or len(raw) < 22:
        return []
    slots: list[tuple[int, int, int]] = []
    position = 10
    while position + 12 <= len(raw):
        slot, start, length = struct.unpack("<III", raw[position:position + 12])
        position += 12
        if not slot:
            break
        if start <= len(raw) and length <= len(raw) - start:
            slots.append((slot, start, length))
    payloads: list[bytes] = []
    for _slot, start, length in sorted(slots):
        chunk = raw[start:start + length]
        try:
            payloads.append(zlib.decompress(chunk))
        except zlib.error:
            payloads.append(chunk)
    return payloads


def _compressed_payloads(raw: bytes) -> list[bytes]:
    rpc2_payloads = _rpc2_payloads(raw)
    if rpc2_payloads:
        return rpc2_payloads
    payloads = []
    if raw.startswith(b"RENPY RPC"):
        raise CompiledReadError("slots RPC2 inválidos")
    candidates = [raw]
    candidates.extend(raw[index:] for index in range(len(raw)) if raw[index:index + 2] in (b"x\x01", b"x\x9c", b"x\xda"))
    for candidate in candidates:
        try:
            payload = zlib.decompress(candidate)
        except zlib.error:
            continue
        if payload not in payloads:
            payloads.append(payload)
    if not payloads:
        raise CompiledReadError("bloco zlib não encontrado")
    return payloads


def read_compiled(path: str | Path) -> Any:
    file_path = Path(path)
    if file_path.suffix.lower() not in {".rpyc", ".rpymc"}:
        raise CompiledReadError("extensão não suportada")
    try:
        raw = file_path.read_bytes()
        errors: list[Exception] = []
        for payload in _compressed_payloads(raw):
            try:
                return SafeRenpyUnpickler(io.BytesIO(payload)).load()
            except (EOFError, pickle.UnpicklingError) as error:
                errors.append(error)
        raise CompiledReadError(str(errors[-1]) if errors else "payload pickle inválido")
    except (OSError, EOFError, pickle.UnpicklingError, zlib.error) as error:
        raise CompiledReadError(str(error)) from error


_TEXT_FIELDS = {"text", "what", "caption", "label", "prompt", "message",
                "title", "description", "tooltip", "help", "content", "value"}


def _repair_mojibake(value: str) -> str:
    if not any(marker in value for marker in ("Ã", "Â", "â", "ð")):
        return value
    try:
        repaired = value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value
    return repaired if repaired.count("�") <= value.count("�") else value


def _strings(node: Any, context: str = "", seen: set[int] | None = None) -> Iterator[tuple[str, int, str]]:
    seen = seen or set()
    if node is None or isinstance(node, (bytearray, int, float, bool)):
        return
    if isinstance(node, bytes):
        for encoding in ("utf-8", "cp1252", "latin-1"):
            try:
                decoded = node.decode(encoding)
            except UnicodeDecodeError:
                continue
            if decoded.strip():
                yield _repair_mojibake(decoded), 0, context
            return
        return
    if isinstance(node, str):
        if node.strip():
            yield _repair_mojibake(node), 0, context
        return
    if id(node) in seen:
        return
    seen.add(id(node))
    if isinstance(node, dict):
        for key, value in node.items():
            key_name = str(key).lower()
            if key_name in _TEXT_FIELDS and isinstance(value, str):
                yield from _strings(value, f"{context}/{key_name}", seen)
            elif not isinstance(value, str):
                yield from _strings(value, f"{context}/{key_name}", seen)
        return
    if isinstance(node, (list, tuple, set)):
        for value in node:
            yield from _strings(value, context, seen)
        return
    for key, value in vars(node).items():
        if key.startswith("_") and key not in {"_text"}:
            continue
        if isinstance(value, str) and key.lower() not in _TEXT_FIELDS:
            continue
        yield from _strings(value, f"{context}/{key}", seen)


def extract_compiled_entries(path: str | Path, relative_to: str | Path | None = None) -> list[TranslationEntry]:
    root = Path(path)
    try:
        payload = read_compiled(root)
    except CompiledReadError:
        return []
    base = Path(relative_to) if relative_to else root.parent
    try:
        file_name = root.relative_to(base).as_posix()
    except ValueError:
        file_name = root.name
    entries: list[TranslationEntry] = []
    seen: set[str] = set()
    for text, line, context in _strings(payload):
        candidate = text.strip()
        if len(candidate) < 2 or candidate in seen or "\x00" in candidate:
            continue
        seen.add(candidate)
        entry_type = "compiled_ui" if any(part in context for part in ("text", "label", "caption")) else "compiled"
        entries.append(TranslationEntry(
            original_text=text,
            file_path=file_name,
            line_number=line,
            entry_type=entry_type,
            context_path=context.strip("/"),
            translation_id=build_translation_id(
                original_text=text, file_path=file_name,
                context_path=context, entry_type=entry_type,
            ),
        ))
    return entries
