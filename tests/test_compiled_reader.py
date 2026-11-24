import pickle
import zlib
from pathlib import Path

from core.compiled_reader import extract_compiled_entries, read_compiled
from core.text_source_parser import extract_translation_entries


def _write_payload(path: Path, value, header: bytes = b"") -> None:
    path.write_bytes(header + zlib.compress(pickle.dumps(value)))


def test_reads_synthetic_rpyc_payload(tmp_path):
    path = tmp_path / "script.rpyc"
    _write_payload(path, {"what": "Hello compiled world", "line": 12})
    entries = extract_compiled_entries(path, tmp_path)
    assert [entry.original_text for entry in entries] == ["Hello compiled world"]


def test_repairs_mojibake_in_compiled_text(tmp_path):
    path = tmp_path / "script.rpyc"
    _write_payload(path, {"what": "Meu nome Ã© Alice"})

    entries = extract_compiled_entries(path, tmp_path)

    assert [entry.original_text for entry in entries] == ["Meu nome é Alice"]


def test_reads_rpc2_slot_and_rpymc(tmp_path):
    payload = zlib.compress(pickle.dumps({"text": "Start"}))
    start = 10 + 12 + 12
    header = b"RENPY RPC2" + struct_pack(1, start, len(payload)) + struct_pack(0, 0, 0)
    path = tmp_path / "screen.rpymc"
    path.write_bytes(header + payload)
    assert read_compiled(path)["text"] == "Start"


def test_reads_rpc2_when_first_slot_is_not_the_pickle_payload(tmp_path):
    first = zlib.compress(b"not a pickle")
    payload = zlib.compress(pickle.dumps({"text": "Second slot"}))
    start = 10 + 12 + 12 + 12
    header = (
        b"RENPY RPC2"
        + struct_pack(1, start, len(first))
        + struct_pack(2, start + len(first), len(payload))
        + struct_pack(0, 0, 0)
    )
    path = tmp_path / "variant.rpyc"
    path.write_bytes(header + first + payload)
    assert read_compiled(path)["text"] == "Second slot"


def test_reads_rpc2_with_uncompressed_slot(tmp_path):
    payload = pickle.dumps({"what": "Uncompressed slot"})
    start = 10 + 12 + 12
    header = b"RENPY RPC2" + struct_pack(1, start, len(payload)) + struct_pack(0, 0, 0)
    path = tmp_path / "plain.rpyc"
    path.write_bytes(header + payload)
    assert read_compiled(path)["what"] == "Uncompressed slot"


def test_rejects_reduce_callable_without_executing(tmp_path):
    class Evil:
        def __reduce__(self):
            import os
            return os.system, ("this must not run",)
    path = tmp_path / "evil.rpyc"
    _write_payload(path, Evil())
    assert extract_compiled_entries(path, tmp_path) == []


def test_parser_prefers_source_rpy_over_matching_compiled_file(tmp_path):
    game = tmp_path / "game"
    game.mkdir()
    (game / "script.rpy").write_text(
        'label start:\n    e "Source text"\n',
        encoding="utf-8",
    )
    _write_payload(game / "script.rpyc", {"what": "Compiled duplicate"})

    entries = extract_translation_entries(game)

    assert [entry.original_text for entry in entries] == ["Source text"]


def struct_pack(slot, start, length):
    import struct
    return struct.pack("<III", slot, start, length)
