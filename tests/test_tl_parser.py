import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from core.tl_parser import parse_tl_directory, parse_tl_file, pending_translation_blocks


class TlParserTests(unittest.TestCase):
    def test_parse_tl_file_reads_completed_and_pending_blocks(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "strings.rpy"
            path.write_text(
                'translate portuguese strings:\n'
                '    old "Start \\\"now\\\""\n'
                '    new "Começar agora"\n\n'
                '    old "Leave\\nnow"\n'
                '    new ""\n',
                encoding="utf-8",
            )

            blocks = parse_tl_file(path)

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].old_text, 'Start "now"')
        self.assertEqual(blocks[0].new_text, "Começar agora")
        self.assertFalse(blocks[0].is_pending)
        self.assertEqual(blocks[1].old_text, "Leave\nnow")
        self.assertTrue(blocks[1].is_pending)

    def test_parse_tl_directory_and_filter_pending_blocks(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "a.rpy").write_text(
                'translate portuguese strings:\n    old "One"\n    new "Um"\n',
                encoding="utf-8",
            )
            (root / "nested").mkdir()
            (root / "nested" / "b.rpy").write_text(
                'translate portuguese strings:\n    old "Two"\n    new ""\n',
                encoding="utf-8",
            )

            blocks = parse_tl_directory(root)
            pending = pending_translation_blocks(root)

        self.assertEqual([block.old_text for block in blocks], ["One", "Two"])
        self.assertEqual([block.old_text for block in pending], ["Two"])


if __name__ == "__main__":
    unittest.main()
