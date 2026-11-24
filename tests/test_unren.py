import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from src.gui import app_backend


class UnrenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = app_backend.AppBackend()
        self.backend._project = ""

    def test_counts_supported_files_and_ignores_missing_game_folder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            (game / "archive.rpa").touch()
            (game / "script.rpyc").touch()
            (game / "module.rpymc").touch()
            self.backend._project = str(root)

            self.assertEqual(self.backend._unren_counts(), (1, 1, 1))

        self.backend._project = str(Path(temp_dir) / "missing")
        self.assertEqual(self.backend._unren_counts(), (0, 0, 0))

    def test_inspect_unren_requires_project(self) -> None:
        self.assertEqual(
            self.backend.inspectUnren(),
            "Selecione um projeto antes de usar o UnRen.",
        )

    def test_inspect_unren_reports_counts_and_tool(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            (game / "archive.rpa").touch()
            (game / "script.rpyc").touch()
            self.backend._project = str(root)

            summary = self.backend.inspectUnren()

        self.assertIn("1 .rpa", summary)
        self.assertIn("1 .rpyc", summary)
        self.assertIn("ferramenta encontrada", summary)

    def test_invalid_option_is_rejected_without_starting_process(self) -> None:
        self.backend._project = "C:\\game"

        with patch.object(app_backend, "QProcess") as process:
            self.assertFalse(self.backend.runUnrenOption(9))
            process.assert_not_called()

    def test_option_one_requires_an_rpa_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "game").mkdir()
            self.backend._project = str(root)

            with patch.object(app_backend, "QProcess") as process:
                self.assertFalse(self.backend.runUnrenOption(1))
                process.assert_not_called()

    def test_option_one_uses_relative_tool_command(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            (game / "archive.rpa").touch()
            self.backend._project = str(root)
            fake_process = MagicMock()

            with patch.object(app_backend, "QProcess", return_value=fake_process):
                self.assertTrue(self.backend.runUnrenOption(1))

            command = fake_process.setArguments.call_args.args[0][2]
            self.assertIn("call UnRen-1.0.11d.bat", command)
            self.assertNotIn(str(root), command)
            self.backend._unren_finished(0, None)

    def test_missing_tool_is_reported(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "game").mkdir()
            self.backend._project = str(root)

            with patch.object(
                Path,
                "is_file",
                autospec=True,
                side_effect=lambda path: path.name != "UnRen-1.0.11d.bat",
            ):
                self.assertFalse(self.backend.runUnrenOption(3))

        self.assertIn("ferramenta não encontrada", self.backend.logs)

    def test_options_three_to_seven_send_their_menu_values(self) -> None:
        for option in range(3, 8):
            with self.subTest(option=option), TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / "game").mkdir()
                self.backend._project = str(root)
                fake_process = MagicMock()

                with patch.object(app_backend, "QProcess", return_value=fake_process):
                    self.assertTrue(self.backend.runUnrenOption(option))

                command = fake_process.setArguments.call_args.args[0][2]
                self.assertIn("call UnRen-1.0.11d.bat", command)
                self.assertNotIn(str(root), command)
                self.backend._unren_finished(0, None)

    def test_option_two_accepts_rpyc_or_rpymc(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            (game / "module.rpymc").touch()
            self.backend._project = str(root)
            fake_process = MagicMock()

            with patch.object(app_backend, "QProcess", return_value=fake_process):
                self.assertTrue(self.backend.runUnrenOption(2))

            arguments = fake_process.setArguments.call_args.args[0]
            self.assertIn("call UnRen-1.0.11d.bat", arguments[2])
            self.assertNotIn(str(root), arguments[2])
            self.assertTrue((root / ".alice" / "unren-backups").is_dir())
            launcher = root / "alice_unren_launcher.py"
            self.assertIn("import renpy.object", launcher.read_text(encoding="ascii"))
            self.assertIn(
                '"%maindir%alice_unren_launcher.py" "%unrpycpy%"',
                (root / "UnRen-1.0.11d.bat").read_text(encoding="utf-8"),
            )
            self.backend._unren_finished(0, None)
            self.assertFalse((root / "UnRen-1.0.11d.bat").exists())
            self.assertFalse(launcher.exists())

    def test_sends_selected_option_through_process_stdin(self) -> None:
        process = MagicMock()
        self.backend._unren_process = process
        self.backend._unren_option = 2

        self.backend._send_unren_input()

        process.write.assert_called_once_with(b"2\r\n\r\n")
        process.closeWriteChannel.assert_called_once_with()

    def test_backup_preserves_supported_files_and_excludes_alice(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            source = game / "nested" / "script.rpy"
            source.parent.mkdir()
            source.write_text("label start:", encoding="utf-8")
            (game / "archive.rpa").touch()
            (game / "compiled.rpyc").touch()
            alice_file = root / ".alice" / "cache.rpy"
            alice_file.parent.mkdir()
            alice_file.touch()
            self.backend._project = str(root)
            fake_process = MagicMock()

            with patch.object(app_backend, "QProcess", return_value=fake_process):
                self.assertTrue(self.backend.runUnrenOption(8))

            backup_root = next((root / ".alice" / "unren-backups").iterdir())
            self.assertEqual(
                (backup_root / "game" / "nested" / "script.rpy").read_text(encoding="utf-8"),
                "label start:",
            )
            self.assertTrue((backup_root / "game" / "archive.rpa").exists())
            self.assertTrue((backup_root / "game" / "compiled.rpyc").exists())
            self.assertFalse((backup_root / ".alice").exists())
            self.backend._unren_finished(0, None)

    def test_run_is_blocked_without_project_or_while_running(self) -> None:
        with patch.object(app_backend, "QProcess") as process:
            self.assertFalse(self.backend.runUnrenOption(3))
            process.assert_not_called()

        self.backend._project = "C:\\game"
        self.backend._unren_process = MagicMock()
        self.assertFalse(self.backend.runUnrenOption(3))

    def test_cancel_unren_kills_running_process(self) -> None:
        process = MagicMock()
        self.backend._unren_process = process

        self.backend.cancelUnren()

        process.kill.assert_called_once_with()

    def test_finished_stops_timeout_and_reports_backup(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "game").mkdir()
            self.backend._project = str(root)
            self.backend._unren_process = MagicMock()
            self.backend._unren_option = 3
            self.backend._unren_backup_dir = root / ".alice" / "unren-backups" / "run"
            self.backend._unren_backup_dir.mkdir(parents=True)
            self.backend._unren_timeout_timer.start()

            self.backend._unren_finished(0, None)

            self.assertFalse(self.backend._unren_timeout_timer.isActive())
            self.assertIn("opção 3 concluído com sucesso", self.backend.unrenSummary)
            self.assertIn("Backup:", self.backend.unrenSummary)


if __name__ == "__main__":
    unittest.main()
