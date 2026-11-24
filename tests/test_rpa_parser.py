import pickle
import struct
import zlib

from core.rpa_parser import RPAParser
from core.rpa_adapter import RPAAdapter


def _write_rpa(path, filename=b"game/script.rpy", content=b'label start:\n'):
    key = 0x1234
    header = b"RPA-3.0 0000000000000000 00001234\n"
    payload_offset = len(header)
    index = {filename: [(payload_offset ^ key, len(content) ^ key, b"")]}
    index_data = zlib.compress(pickle.dumps(index))
    index_offset = payload_offset + len(content)
    header = f"RPA-3.0 {index_offset:016x} {key:08x}\n".encode("ascii")
    path.write_bytes(header + content + index_data)


def test_extracts_rpa3_without_unrpa(tmp_path, monkeypatch):
    archive = tmp_path / "archive.rpa"
    _write_rpa(archive)
    monkeypatch.setattr("core.rpa_adapter.RPAParser", RPAParser)
    assert RPAParser().extract_archive(archive, tmp_path / "game")
    assert (tmp_path / "game" / "game" / "script.rpy").read_bytes() == b"label start:\n"


def test_finds_rpa_case_insensitively(tmp_path):
    game = tmp_path / "game"
    game.mkdir()
    (game / "DATA.RPA").touch()
    assert RPAAdapter.find_archives(game) == [game / "DATA.RPA"]


def test_rejects_path_traversal(tmp_path):
    archive = tmp_path / "archive.rpa"
    key = 0
    header = b"RPA-2.0 0000000000000000\n"
    payload = b"safe"
    index = {b"../outside.txt": [(len(header) ^ key, len(payload) ^ key, b"")]}
    index_offset = len(header) + len(payload)
    header = f"RPA-2.0 {index_offset:016x}\n".encode("ascii")
    archive.write_bytes(header + payload + zlib.compress(pickle.dumps(index)))
    assert not RPAParser().extract_archive(archive, tmp_path / "game")
    assert not (tmp_path / "outside.txt").exists()
