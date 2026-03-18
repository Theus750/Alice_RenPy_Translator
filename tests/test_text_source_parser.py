import unittest
from pathlib import Path

from syntax_guard import protect_placeholders, restore_placeholders
from text_source_parser import extract_translation_entries


class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures_path = Path(__file__).parent / "fixtures"

    def test_extracts_expected_entry_count(self) -> None:
        entries = extract_translation_entries(str(self.fixtures_path))
        self.assertEqual(len(entries), 13)
        self.assertEqual(entries[0].speaker, "e")
        self.assertEqual(entries[0].entry_type, "dialogue")
        self.assertTrue(
            any(entry.original_text == "This was inside parentheses" for entry in entries)
        )
        self.assertTrue(any(entry.original_text == "Localized dialogue" for entry in entries))
        self.assertTrue(any(entry.original_text == "Localized narration" for entry in entries))
        self.assertTrue(any(entry.original_text == "Leave now" for entry in entries))
        self.assertTrue(
            any(entry.original_text == "Nested localized dialogue" for entry in entries)
        )
        self.assertTrue(
            any(
                entry.original_text == "Localized single quote dialogue"
                for entry in entries
            )
        )
        self.assertTrue(
            any(
                entry.original_text == "Localized single quote narration"
                for entry in entries
            )
        )
        self.assertTrue(any(entry.original_text == "Leave single quote" for entry in entries))
        self.assertTrue(
            any(entry.original_text == "Nested single quote dialogue" for entry in entries)
        )

    def test_translation_ids_are_stable(self) -> None:
        first = extract_translation_entries(str(self.fixtures_path))
        second = extract_translation_entries(str(self.fixtures_path))

        first_ids = [entry.translation_id for entry in first]
        second_ids = [entry.translation_id for entry in second]
        self.assertEqual(first_ids, second_ids)

    def test_placeholder_roundtrip(self) -> None:
        text = "Hello [player], score {points}, raw %s"
        protected, placeholders = protect_placeholders(text)
        restored = restore_placeholders(protected, placeholders)

        self.assertEqual(text, restored)


if __name__ == "__main__":
    unittest.main()
