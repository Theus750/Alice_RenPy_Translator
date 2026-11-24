import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from config_manager import AppConfig, ConfigManager
import run_cli
import cli.run_cli as cli_run
from run_cli import _infer_renpy_language, _resolve_relative_path
from translation_pipeline import TranslationPipeline


class ConfigAndPathTests(unittest.TestCase):
    def test_config_manager_loads_defaults_when_missing(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            manager = ConfigManager(config_path)

            config = manager.load()

        self.assertEqual(config.project.project_path, "")
        self.assertEqual(config.translation.selected_engine, "libretranslate")
        self.assertEqual(config.ui.locale, "pt-BR")

    def test_config_manager_roundtrip(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            manager = ConfigManager(config_path)
            original = AppConfig()
            original.project.project_path = r"C:\Games\MeuJogo"
            original.translation.target_language = "es"
            original.ui.locale = "es"

            manager.save(original)
            loaded = manager.load()

        self.assertEqual(loaded.project.project_path, r"C:\Games\MeuJogo")
        self.assertEqual(loaded.translation.target_language, "es")
        self.assertEqual(loaded.ui.locale, "es")

    def test_config_manager_sections_are_gui_friendly(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            manager = ConfigManager(config_path)

            sections = manager.sections()

        self.assertEqual(set(sections.keys()), {"project", "translation", "ui"})
        self.assertIn("project_path", sections["project"])
        self.assertIn("target_language", sections["translation"])
        self.assertIn("theme", sections["ui"])

    def test_update_section_persists_partial_changes(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            manager = ConfigManager(config_path)

            manager.update_section("ui", {"theme": "dark", "locale": "es"})
            loaded = manager.load()

        self.assertEqual(loaded.ui.theme, "dark")
        self.assertEqual(loaded.ui.locale, "es")

    def test_cli_edit_config_saves_values(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            argv = [
                "run_cli.py",
                "--config",
                str(config_path),
                "--edit-config",
                "--set-theme",
                "dark",
                "--set-last-opened-project",
                r"C:\Games\MeuJogo",
            ]

            with patch.object(cli_run.sys, "argv", argv), patch.object(
                cli_run,
                "translate_raw_text",
                side_effect=lambda text, **_kwargs: text,
            ), patch.object(
                cli_run,
                "translate_raw_texts",
                side_effect=lambda texts, **_kwargs: list(texts),
            ):
                with redirect_stdout(io.StringIO()):
                    run_cli.main()

            saved = ConfigManager(config_path).load()

        self.assertEqual(saved.ui.theme, "dark")
        self.assertEqual(saved.ui.last_opened_project, r"C:\Games\MeuJogo")

    def test_cli_can_skip_language_file_generation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            (game_path / "script.rpy").write_text('label start:\n    e "Hello"\n', encoding="utf-8")

            argv = [
                "run_cli.py",
                str(root_path),
                "--skip-language-file",
            ]

            with patch.object(cli_run.sys, "argv", argv), patch.object(
                cli_run,
                "translate_raw_text",
                side_effect=lambda text, **_kwargs: text,
            ), patch.object(
                cli_run,
                "translate_raw_texts",
                side_effect=lambda texts, **_kwargs: list(texts),
            ):
                with redirect_stdout(io.StringIO()):
                    run_cli.main()

            self.assertFalse((game_path / "zzz_alice_language.rpy").exists())

    def test_resolve_relative_path_handles_relative_and_absolute_values(self) -> None:
        base_path = Path(r"C:\Base")
        relative = _resolve_relative_path(base_path, "folder/output.json")
        absolute = _resolve_relative_path(base_path, r"C:\Other\output.json")

        self.assertEqual(relative, Path(r"C:\Base\folder\output.json"))
        self.assertEqual(absolute, Path(r"C:\Other\output.json"))

    def test_translation_pipeline_resolves_project_root_from_game_folder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()

            pipeline = TranslationPipeline(project_path=str(root_path), output_path="")
            nested = TranslationPipeline(project_path=str(game_path), output_path="")

        self.assertEqual(pipeline.project_root, root_path)
        self.assertEqual(pipeline.game_path, game_path)
        self.assertEqual(nested.project_root, root_path)
        self.assertEqual(nested.game_path, game_path)

    def test_translation_pipeline_requires_source_rpy_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            game_path = Path(temp_dir) / "game"
            (game_path / "tl" / "portuguese").mkdir(parents=True)
            (game_path / "tl" / "portuguese" / "strings.rpy").write_text(
                "translate portuguese strings:\n",
                encoding="utf-8",
            )

            pipeline = TranslationPipeline(project_path=temp_dir, output_path="")

            with self.assertRaisesRegex(FileNotFoundError, "Nenhum arquivo .rpy"):
                pipeline.run()

    def test_infer_renpy_language_uses_output_folder_name(self) -> None:
        config = AppConfig()
        config.project.dialogue_output_path = "game/tl/portuguese/dialogue.rpy"

        self.assertEqual(_infer_renpy_language(config), "portuguese")

    def test_infer_renpy_language_replaces_hyphens(self) -> None:
        config = AppConfig()
        config.project.dialogue_output_path = "game/tl/pt-BR/dialogue.rpy"

        self.assertEqual(_infer_renpy_language(config), "pt_BR")

    def test_translation_pipeline_emits_progress_logs(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            script = game_path / "script.rpy"
            script.write_text('label start:\n    e "Hello"\n', encoding="utf-8")

            pipeline = TranslationPipeline(project_path=str(root_path), output_path=str(root_path / "extracted_entries.json"))

            with self.assertLogs("core.translation_pipeline", level="INFO") as logs:
                result = pipeline.run(
                    translator=lambda text: f"pt::{text}",
                    cache={},
                    language="portuguese",
                )

            self.assertTrue(result.output_file.exists())
            self.assertIsNotNone(result.language_file)
            self.assertTrue(result.language_file.exists())
            self.assertEqual(result.language_file.name, "zzz_alice_language.rpy")
            self.assertTrue(any("Iniciando tradução de" in message for message in logs.output))
            self.assertTrue(any("traduzindo:" in message for message in logs.output))
            self.assertTrue(any("Arquivos gerados" in message for message in logs.output))

    def test_translation_pipeline_removes_spurious_terminal_quote(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            (game_path / "script.rpy").write_text(
                'label start:\n'
                '    l "It ends normally"\n',
                encoding="utf-8",
            )
            pipeline = TranslationPipeline(
                project_path=str(root_path),
                output_path=str(root_path / "extracted_entries.json"),
            )

            result = pipeline.run(
                translator=lambda text: f"{text} \"",
                cache={},
                language="portuguese",
            )

        self.assertEqual(result.translations[result.entries[0].translation_id], "It ends normally")

    def test_translation_pipeline_retranslates_cache_values_equal_to_source(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            (game_path / "script.rpy").write_text(
                'label start:\n'
                '    e "You remember this [name]?"\n',
                encoding="utf-8",
            )
            calls = []
            pipeline = TranslationPipeline(
                project_path=str(root_path),
                output_path=str(root_path / "extracted_entries.json"),
            )

            result = pipeline.run(
                translator=lambda text: calls.append(text)
                or text.replace("You remember this", "Você se lembra disso"),
                cache={"You remember this [name]?": "You remember this [name]?"},
                language="portuguese",
            )

            self.assertEqual(calls, ["You remember this ", "?"])
            translation_id = result.entries[0].translation_id
            self.assertEqual(
                result.translations[translation_id],
                "Você se lembra disso [name]?",
            )

    def test_translation_pipeline_repairs_missing_placeholder_spacing(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            original = "All your junk stayed in your room in [fName.normal]'s house."
            (game_path / "script.rpy").write_text(
                f'label start:\n    e "{original}"\n',
                encoding="utf-8",
            )
            pipeline = TranslationPipeline(
                project_path=str(root_path),
                output_path=str(root_path / "extracted_entries.json"),
            )

            result = pipeline.run(
                translator=lambda text: {
                    "All your junk stayed in your room in ": "Todo o seu lixo ficou em seu quarto em",
                    "'s house.": "é a casa.",
                }[text],
                cache={original: "Todo o seu lixo ficou em seu quarto em[fName.normal]é a casa."},
                language="portuguese",
            )

            translation_id = result.entries[0].translation_id
            self.assertEqual(
                result.translations[translation_id],
                "Todo o seu lixo ficou em seu quarto em [fName.normal] é a casa.",
            )

    def test_translation_pipeline_preserves_placeholder_before_punctuation(self) -> None:
            with TemporaryDirectory() as temp_dir:
                root_path = Path(temp_dir)
                game_path = root_path / "game"
                game_path.mkdir()
                original = "Good morning. You must be [player_name]. Please, come in."
                (game_path / "script.rpy").write_text(
                    f'label start:\n    e "{original}"\n',
                    encoding="utf-8",
                )
                pipeline = TranslationPipeline(
                    project_path=str(root_path),
                    output_path=str(root_path / "extracted_entries.json"),
                )

                def translator(text):
                    return {
                        "Good morning. You must be ": "Bom dia. Você deve ser",
                        ". Please, come in.": ". Por favor, entre.",
                    }[text]

                result = pipeline.run(
                    translator=translator,
                    cache={},
                    language="portuguese",
                )

            translation_id = result.entries[0].translation_id
            self.assertEqual(
                result.translations[translation_id],
                "Bom dia. Você deve ser [player_name]. Por favor, entre.",
            )

    def test_translation_pipeline_preserves_unicode_ellipsis_after_placeholder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            original = "Hi, [player_name]… come closer."
            (game_path / "script.rpy").write_text(
                f'label start:\n    e "{original}"\n',
                encoding="utf-8",
            )
            pipeline = TranslationPipeline(
                project_path=str(root_path),
                output_path=str(root_path / "extracted_entries.json"),
            )

            def translator(text):
                return {
                    "Hi, ": "Olá, ",
                    "… come closer.": "chegue mais perto.",
                }[text]

            result = pipeline.run(
                translator=translator,
                cache={},
                language="portuguese",
            )

            translation_id = result.entries[0].translation_id
            self.assertEqual(
                result.translations[translation_id],
                "Olá, [player_name]… chegue mais perto.",
            )

    def test_cli_purges_invalid_cache_entries_before_translation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            cache_path = root_path / "cache.json"
            cache_path.write_text(
                '{"Look elsewhere [heroname], what are you thinking about?": '
                '"Procure em outro lugar[heroname]no que está pensando?",'
                '"Did you actually enjoy this spectacle, [player_name]? ": '
                '"Did you actually enjoy this spectacle, [player_name]? "}',
                encoding="utf-8",
            )
            config_path = root_path / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "project": {
                            "project_path": str(root_path),
                            "cache_path": str(cache_path),
                        }
                    }
                ),
                encoding="utf-8",
            )
            game_path = root_path / "game"
            game_path.mkdir()
            (game_path / "script.rpy").write_text(
                'label start:\n    e "Hello"\n',
                encoding="utf-8",
            )

            argv = ["run_cli.py", "--config", str(config_path), str(root_path)]
            with patch.object(run_cli.sys, "argv", argv):
                with patch.object(cli_run, "translate_raw_text", return_value="Olá"):
                    with patch.object(cli_run, "translate_raw_texts", return_value=["Olá"]):
                        with redirect_stdout(io.StringIO()):
                            run_cli.main()

            cache = json.loads(cache_path.read_text(encoding="utf-8"))
            self.assertNotIn(
                "Look elsewhere [heroname], what are you thinking about?",
                cache,
            )
            self.assertNotIn(
                "Did you actually enjoy this spectacle, [player_name]? ",
                cache,
            )

    def test_translation_pipeline_rejects_incomplete_batch_results(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root_path = Path(temp_dir)
            game_path = root_path / "game"
            game_path.mkdir()
            (game_path / "script.rpy").write_text(
                'label start:\n'
                '    e "First"\n'
                '    e "Second"\n',
                encoding="utf-8",
            )
            pipeline = TranslationPipeline(project_path=str(root_path), output_path="")

            with self.assertRaisesRegex(ValueError, "quantidade de traduções"):
                pipeline.run(
                    translator=lambda text: text,
                    batch_translator=lambda texts: ["only one"],
                    cache={},
                )


if __name__ == "__main__":
    unittest.main()