import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from dialogue_output import save_dialogue_rpy, save_language_rpy, save_strings_rpy
from syntax_guard import protect_placeholders, restore_placeholders
from text_source_parser import extract_translation_entries, find_named_menus


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

    def test_extracts_menu_caption_as_string(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    menu:\n'
                '        "Who do you apply sunscreen to first?"\n'
                '        "Rachel":\n'
                '            jump rachel\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].entry_type, "menu_caption")
        self.assertEqual(entries[1].entry_type, "menu_choice")

    def test_extracts_renpy_input_prompt_as_string(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    $ player_name = renpy.input("What is your name (default is Alan)?")\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].entry_type, "input_string")
        self.assertEqual(entries[0].original_text, "What is your name (default is Alan)?")

    def test_extracts_screen_strings_outside_labels(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "screens.rpy"
            fixture.write_text(
                'screen navigation():\n'
                '    textbutton _("Start") action Start()\n'
                '    textbutton _(\'Quit\') action Quit()\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual([entry.original_text for entry in entries], ["Start", "Quit"])
        self.assertTrue(all(entry.entry_type == "screen_string" for entry in entries))

    def test_placeholder_roundtrip(self) -> None:
        text = "Hello [player], score {points}, raw %s"
        protected, placeholders = protect_placeholders(text)
        restored = restore_placeholders(protected, placeholders)

        self.assertEqual(text, restored)

    def test_renpy_escape_roundtrip(self) -> None:
        text = r"\n\nThe second day in the morning"
        protected, placeholders = protect_placeholders(text)
        self.assertEqual(placeholders, [r"\n", r"\n"])
        self.assertEqual(restore_placeholders(protected, placeholders), text)

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
        self.assertIn('old "Go to beach"', content)
        self.assertIn('new "pt::Go to beach"', content)
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

    def test_save_dialogue_rpy_uses_named_menu_in_identifier(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    menu named_choice:\n'
                '        "Yes":\n'
                '            e "Nested dialogue"\n'
                '    e "After named menu"\n',
                encoding="utf-8",
            )
            entries = extract_translation_entries(temp_dir)
            translations = {entry.translation_id: f"pt::{entry.original_text}" for entry in entries}
            output_path = Path(temp_dir) / "dialogue.rpy"
            save_dialogue_rpy(entries, translations, output_path=str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("translate portuguese named_choice_", content)

    def test_save_dialogue_rpy_normalizes_repeated_spaces_in_identifier(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label introduction:\n'
                '    ga "But at the last minute, Lucy, Rachel\'s daughter,  joins as well."\n',
                encoding="utf-8",
            )
            entries = extract_translation_entries(temp_dir)
            translations = {entry.translation_id: "Lucy se junta tambem." for entry in entries}
            output_path = Path(temp_dir) / "dialogue.rpy"
            save_dialogue_rpy(entries, translations, output_path=str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("translate portuguese introduction_", content)
        self.assertIn("bdea9ca6", content)

    def test_save_dialogue_rpy_preserves_renpy_escape_sequences(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    centered "\\n\\nMorning at the beach"\n',
                encoding="utf-8",
            )
            entries = extract_translation_entries(temp_dir)
            translations = {entry.translation_id: r"\n\nManhã na praia" for entry in entries}
            output_path = Path(temp_dir) / "dialogue.rpy"
            save_dialogue_rpy(entries, translations, output_path=str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn('    centered "\\n\\nManhã na praia"', content)
        self.assertNotIn('    centered "\\\\n\\\\nManhã na praia"', content)

    def test_save_language_rpy_writes_config_language(self) -> None:
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "zzz_portuguese_language.rpy"
            save_language_rpy("portuguese", str(output_path))
            content = output_path.read_text(encoding="utf-8")

        self.assertIn('define config.language = "portuguese"', content)

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

    def test_detects_named_menus(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    menu named_choice:\n'
                '        "Yes":\n'
                '            jump yes\n',
                encoding="utf-8",
            )

            menus = find_named_menus(temp_dir)

        self.assertEqual(menus[0].name, "named_choice")
        self.assertEqual(menus[0].line_number, 2)

    def test_extracts_dialogue_starting_with_placeholder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label night1:\n'
                '    l "[player_name], I am exhausted. Can we rest?"\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].original_text, "[player_name], I am exhausted. Can we rest?")

    def test_extracts_dialogue_without_space_after_speaker(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "script.rpy"
            fixture.write_text(
                'label start:\n'
                '    l"Hey, [player_name]! Can I borrow her for a moment?"\n',
                encoding="utf-8",
            )

            entries = extract_translation_entries(temp_dir)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].speaker, "l")
        self.assertEqual(
            entries[0].original_text,
            "Hey, [player_name]! Can I borrow her for a moment?",
        )


if __name__ == "__main__":
    unittest.main()
