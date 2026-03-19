import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from dialogue_output import save_dialogue_rpy, save_strings_rpy
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

    def test_placeholder_restore_handles_mutated_tokens(self) -> None:
        text = "__VAR0_(italic)__VAR1_"
        restored = restore_placeholders(text, ["{i}", "{/i}"])

        self.assertEqual(restored, "{i}(italic){/i}")

    def test_placeholder_restore_handles_bracketed_tokens(self) -> None:
        text = "[[PH_0]] Outro dia calmo no mar.."
        restored = restore_placeholders(text, ["{i}"])

        self.assertEqual(restored, "{i} Outro dia calmo no mar..")

    def test_save_strings_rpy_uses_only_menu_choices(self) -> None:
        entries = extract_translation_entries(str(self.fixtures_path))
        translations = {
            entry.translation_id: f"pt::{entry.original_text}"
            for entry in entries
        }

        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "strings.rpy"
            save_strings_rpy(entries, translations, output_path=str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("translate portuguese strings:", content)
        self.assertIn('old "Leave now"', content)
        self.assertIn('new "pt::Leave now"', content)
        self.assertNotIn('old "Localized dialogue"', content)

    def test_save_dialogue_rpy_uses_renpy_translation_identifiers(self) -> None:
        entries = extract_translation_entries(str(self.fixtures_path))
        translations = {
            entry.translation_id: f"pt::{entry.original_text}"
            for entry in entries
        }

        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "dialogue.rpy"
            save_dialogue_rpy(entries, translations, output_path=str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("translate portuguese start_", content)
        self.assertIn('    # e "Hello [player_name]!"', content)
        self.assertIn('    e "pt::Hello [player_name]!"', content)
        self.assertNotIn("translate portuguese start:", content)
        self.assertIn('    # e ("This was inside parentheses")', content)
        self.assertIn('    e ("pt::This was inside parentheses")', content)

    def test_ignores_screen_language_false_positives_outside_labels(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "screens.rpy"
            fixture.write_text(
                'screen say():\n'
                '    window:\n'
                '        id "window"\n'
                '        text "Name"\n'
                '\n'
                'label start:\n'
                '    e "Real dialogue"\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        texts = [entry.original_text for entry in entries]
        self.assertEqual(texts, ["Real dialogue"])

    def test_extracts_dialogue_with_renpy_text_tags(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    mc "{i}(Did she do it on purpose?){/i}"\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].speaker, "mc")
        self.assertEqual(entries[0].original_text, "{i}(Did she do it on purpose?){/i}")


if __name__ == "__main__":
    unittest.main()
