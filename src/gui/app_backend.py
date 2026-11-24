from pathlib import Path
import json
import csv
import shutil
import re
from datetime import datetime
import sys

from PySide6.QtCore import QObject, Property, QProcess, QProcessEnvironment, QThread, QTimer, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtGui import QGuiApplication

from core.translation_pipeline import TranslationPipeline
from core.translator import (
    load_cache,
    purge_invalid_placeholder_cache,
    save_cache,
    translate_raw_text,
)
from core.config_manager import ConfigManager
from core.dialogue_output import save_dialogue_rpy, save_strings_rpy
from core.translation_entry import TranslationEntry
from core.syntax_guard import placeholders_match, placeholder_spacing_matches
from core.text_source_parser import extract_translation_entries


class PipelineWorker(QObject):
    progress = Signal(str, int, int, str)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.cancel_requested = False

    @Slot()
    def cancel(self):
        self.cancel_requested = True

    @Slot()
    def run(self):
        try:
            def report(stage, current, total, message):
                if self.cancel_requested:
                    raise RuntimeError("Tradução cancelada pelo usuário")
                self.progress.emit(stage, current, total, message)

            config = ConfigManager().load()
            pipeline = TranslationPipeline(self.project, output_path="")
            cache_path = config.project.cache_path
            purge_invalid_placeholder_cache(cache_path)
            cache = load_cache(cache_path)
            result = pipeline.run(
                translator=lambda text: translate_raw_text(text, source=config.translation.source_language, target=config.translation.target_language),
                cache=cache,
                language="portuguese",
                progress_callback=report,
            )
            if self.cancel_requested:
                raise RuntimeError("Tradução cancelada pelo usuário")
            save_cache(cache, cache_path)
            self.finished.emit(result)
        except Exception as error:
            self.failed.emit(str(error))


class AppBackend(QObject):
    projectChanged = Signal()
    statusChanged = Signal()
    countsChanged = Signal()
    logsChanged = Signal()
    progressChanged = Signal()
    filesGeneratedChanged = Signal()
    settingsChanged = Signal()
    reviewChanged = Signal()
    reviewSelectionChanged = Signal()
    glossaryChanged = Signal()
    connectionChanged = Signal()

    def __init__(self):
        super().__init__()
        self._project = ""
        self._status = "Nenhum projeto aberto"
        self._files = 0
        self._entries = 0
        self._logs = "[INFO] Alice pronta."
        self._progress = 0
        self._files_generated = []
        self._thread = None
        self._worker = None
        self._process = None
        self._unren_process = None
        self._unren_summary = "UnRen não verificado."
        self._unren_backup_dir = None
        self._unren_option = None
        self._unren_log_path = None
        self._unren_launcher_path = None
        self._unren_cancel_requested = False
        self._unren_timeout_timer = QTimer(self)
        self._unren_timeout_timer.setSingleShot(True)
        self._unren_timeout_timer.setInterval(10 * 60 * 1000)
        self._unren_timeout_timer.timeout.connect(self.cancelUnren)
        self._cancel_requested = False
        self._connection_status = "Não testado"
        self._diagnostic_summary = "Nenhum diagnóstico executado."
        self._connection_process = None
        self._history = []
        history_path = Path("history.json")
        if history_path.exists():
            try:
                self._history = json.loads(history_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self._history = []
        config = ConfigManager().load()
        self._source_language = config.translation.source_language
        self._target_language = config.translation.target_language
        self._engine = config.translation.selected_engine
        self._api_url = config.translation.api_url
        self._timeout = config.translation.timeout
        self._max_retries = config.translation.max_retries
        self._review_entries = []
        self._review_originals = []
        self._review_translations = []
        self._review_objects = []
        self._review_ids = []
        self._quality = {
            "total": 0,
            "translated": 0,
            "pending": 0,
            "issues": 0,
            "same": 0,
        }
        self._glossary = ConfigManager().load_glossary("glossary.json")
        self._menu_glossary = ConfigManager().load_glossary("menu_glossary.json")
        if config.ui.last_opened_project and Path(config.ui.last_opened_project).exists():
            self.selectProject(config.ui.last_opened_project)

    def _get_project(self):
        return self._project

    def _get_status(self):
        return self._status

    def _get_files(self):
        return self._files

    def _get_entries(self):
        return self._entries

    def _get_logs(self):
        return self._logs

    def _get_progress(self):
        return self._progress

    def _get_files_generated(self):
        return "\n".join(self._files_generated)

    def _get_source_language(self):
        return self._source_language

    def _get_target_language(self):
        return self._target_language

    def _get_engine(self):
        return self._engine

    def _get_review_entries(self):
        return self._review_entries

    def _cache_path(self):
        configured = Path(ConfigManager().load().project.cache_path)
        if configured.is_absolute():
            return configured
        return Path(self._project or ".") / ".alice" / "cache.json"

    project = Property(str, _get_project, notify=projectChanged)
    status = Property(str, _get_status, notify=statusChanged)
    files = Property(int, _get_files, notify=countsChanged)
    entries = Property(int, _get_entries, notify=countsChanged)
    logs = Property(str, _get_logs, notify=logsChanged)
    progress = Property(int, _get_progress, notify=progressChanged)
    translating = Property(
        bool,
        lambda self: self._process is not None
        and self._process.state() != QProcess.NotRunning,
        notify=statusChanged,
    )
    filesGenerated = Property(str, _get_files_generated, notify=filesGeneratedChanged)
    sourceLanguage = Property(str, _get_source_language, notify=settingsChanged)
    targetLanguage = Property(str, _get_target_language, notify=settingsChanged)
    engine = Property(str, _get_engine, notify=settingsChanged)
    apiUrl = Property(str, lambda self: self._api_url, notify=settingsChanged)
    timeout = Property(int, lambda self: self._timeout, notify=settingsChanged)
    maxRetries = Property(int, lambda self: self._max_retries, notify=settingsChanged)
    connectionStatus = Property(str, lambda self: self._connection_status,     notify=connectionChanged
    )
    qualitySummary = Property(
    "QStringList",
    lambda self: [
        f"Total: {self._quality['total']}",
        f"Traduzidas: {self._quality['translated']}",
        f"Pendentes: {self._quality['pending']}",
        f"Com problemas: {self._quality['issues']}",
        f"Iguais ao original: {self._quality['same']}",
    ],
    notify=connectionChanged,)
    diagnosticSummary = Property(str, lambda self: self._diagnostic_summary, notify=connectionChanged)
    unrenSummary = Property(str, lambda self: self._unren_summary, notify=connectionChanged)
    unrenRunning = Property(
        bool,
        lambda self: self._unren_process is not None
        and self._unren_process.state() != QProcess.NotRunning,
        notify=connectionChanged,
    )
    unrenBackupPath = Property(
        str,
        lambda self: str(self._unren_backup_dir or ""),
        notify=connectionChanged,
    )
    unrenStatus = Property(
        str,
        lambda self: self._unren_summary.split(". ", 1)[0],
        notify=connectionChanged,
    )
    cachePath = Property(str, lambda self: str(self._cache_path()), notify=projectChanged)
    historyEntries = Property(
        "QStringList",
        lambda self: [
            f"{item.get('date', '')} | {item.get('project', '')} | "
            f"{item.get('entries', 0)} entradas | "
            f"{item.get('translated', 0)} traduzidas | {item.get('status', '')}"
            for item in self._history
        ],
        notify=connectionChanged,
    )
    reviewEntries = Property("QStringList", _get_review_entries, notify=reviewChanged)
    glossaryEntries = Property("QStringList", lambda self: [f"{key} → {value}" for key, value in self._glossary.items()], notify=glossaryChanged)
    menuGlossaryEntries = Property("QStringList", lambda self: [f"{key} → {value}" for key, value in self._menu_glossary.items()], notify=glossaryChanged)

    def _refresh_quality(self):
        total = len(self._review_originals)
        translated = sum(bool(value.strip()) for value in self._review_translations)
        same = sum(
            bool(value.strip()) and original.strip() == value.strip()
            for original, value in zip(self._review_originals, self._review_translations)
        )
        issues = sum(self.reviewHasIssue(index) for index in range(total))
        self._quality = {
            "total": total,
            "translated": translated,
            "pending": total - translated,
            "issues": issues,
            "same": same,
        }
        self.connectionChanged.emit()

    @Slot(str, str, str)
    def addGlossaryTerm(self, original, translation, context="global"):
        if original.strip() and translation.strip():
            target = self._menu_glossary if context == "menu" else self._glossary
            target[original.strip()] = translation.strip()
            self.glossaryChanged.emit()

    @Slot(str)
    def removeGlossaryTerm(self, entry, context="global"):
        original = entry.split(" → ", 1)[0]
        target = self._menu_glossary if context == "menu" else self._glossary
        target.pop(original, None)
        self.glossaryChanged.emit()

    @Slot()
    def saveGlossary(self):
        manager = ConfigManager()
        manager.save_glossary(self._glossary, "glossary.json")
        manager.save_glossary(self._menu_glossary, "menu_glossary.json")
        self._log(f"Glossários salvos: {len(self._glossary)} global, {len(self._menu_glossary)} de menu.")

    @Slot(str, str)
    def exportGlossary(self, path, context="global"):
        target = self._menu_glossary if context == "menu" else self._glossary
        try:
            output = Path(path)
            if output.suffix.lower() == ".csv":
                with output.open("w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["original", "translation"])
                    writer.writerows(target.items())
            else:
                output.write_text(json.dumps(target, ensure_ascii=False, indent=2), encoding="utf-8")
            self._log(f"Glossário exportado: {path}")
        except (OSError, csv.Error) as error:
            self._log(f"ERROR: não foi possível exportar o glossário: {error}")

    @Slot(str, str)
    def importGlossary(self, path, context="global"):
        try:
            input_path = Path(path)
            if input_path.suffix.lower() == ".csv":
                with input_path.open(newline="", encoding="utf-8") as file:
                    rows = csv.DictReader(file)
                    data = {row["original"]: row["translation"] for row in rows if row.get("original") and row.get("translation")}
            else:
                data = json.loads(input_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("o arquivo deve conter um objeto JSON")
            target = self._menu_glossary if context == "menu" else self._glossary
            target.update({str(key): str(value) for key, value in data.items()})
            self.glossaryChanged.emit()
            self._log(f"Glossário importado: {len(data)} termos.")
        except (OSError, ValueError, TypeError, KeyError, csv.Error) as error:
            self._log(f"ERROR: não foi possível importar o glossário: {error}")

    @Slot()
    def clearProjectCache(self):
        if not self._project:
            self._log("WARNING: selecione um projeto antes de limpar o cache.")
            return
        path = self._cache_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                backup = path.with_name(f"{path.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{path.suffix}")
                shutil.copy2(path, backup)
            save_cache({}, path)
            self._review_entries = []
            self._review_originals = []
            self._review_translations = []
            self._review_objects = []
            self.reviewChanged.emit()
            self._log(f"Cache do projeto limpo: {path}")
        except OSError as error:
            self._log(f"ERROR: não foi possível limpar o cache: {error}")

    @Slot()
    def restoreLatestCacheBackup(self):
        path = self._cache_path()
        backups = sorted(path.parent.glob(f"{path.stem}.backup-*{path.suffix}"), key=lambda item: item.stat().st_mtime, reverse=True)
        if not backups:
            self._log("WARNING: nenhum backup de cache encontrado.")
            return
        try:
            shutil.copy2(backups[0], path)
            self._log(f"Backup restaurado: {backups[0]}")
            self.refreshDiagnostics()
        except OSError as error:
            self._log(f"ERROR: não foi possível restaurar o backup: {error}")

    @Slot()
    def openCacheFolder(self):
        path = self._cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.parent)))
        self._log(f"Pasta do cache aberta: {path.parent}")

    @Slot()
    def testConnection(self):
        self._connection_status = "Testando..."
        self.connectionChanged.emit()
        self._connection_process = QProcess(self)
        self._connection_process.setProgram(sys.executable)
        endpoint = self._api_url.rsplit("/", 1)[0] + "/languages"
        self._connection_process.setArguments(["-c", f"import requests; r=requests.get({endpoint!r}, timeout={self._timeout}); r.raise_for_status(); print('OK')"])
        self._connection_process.finished.connect(self._connection_finished)
        self._connection_process.start()

    @Slot(int, QProcess.ExitStatus)
    def _connection_finished(self, exit_code, _status):
        self._connection_status = "Conectado" if exit_code == 0 else "Falha de conexão"
        self._log(f"LibreTranslate: {self._connection_status}.")
        self.connectionChanged.emit()

    @Slot()
    def refreshDiagnostics(self):
        cache_path = self._cache_path()
        try:
            cache = load_cache(cache_path)
            invalid = purge_invalid_placeholder_cache(cache_path)
            translated = sum(1 for original, value in cache.items() if original != value)
            placeholder_errors = sum(
                1 for original, value in cache.items()
                if not placeholders_match(original, value)
                or not placeholder_spacing_matches(original, value)
            )
            self._diagnostic_summary = (
                f"Arquivo: {cache_path} | Entradas: {len(cache)} | "
                f"traduções diferentes: {translated} | "
                f"placeholders problemáticos: {placeholder_errors} | "
                f"inválidas removidas: {invalid}"
            )
            self._log(self._diagnostic_summary)
        except (OSError, ValueError, TypeError) as error:
            self._diagnostic_summary = f"Falha ao ler cache: {error}"
            self._log(f"ERROR: {self._diagnostic_summary}")
        self.connectionChanged.emit()

    @Slot(result=bool)
    def validateProject(self):
        if not self._project:
            self._diagnostic_summary = "Nenhum projeto selecionado."
            self.connectionChanged.emit()
            return False
        root = Path(self._project)
        game = root / "game"
        issues = []
        if not game.is_dir():
            issues.append("pasta game ausente")
        source_files = [item for item in game.rglob("*.rpy") if "tl" not in item.parts] if game.is_dir() else []
        compiled_files = (
            [
                item for pattern in ("*.rpyc", "*.rpymc")
                for item in game.rglob(pattern)
                if "tl" not in item.parts
            ]
            if game.is_dir()
            else []
        )
        if not source_files and not compiled_files:
            issues.append("nenhum arquivo .rpy, .rpyc ou .rpymc de origem")
        compiled = sum(len(list(game.rglob(pattern))) for pattern in ("*.rpyc", "*.rpa", "*.rpymc")) if game.is_dir() else 0
        self._diagnostic_summary = (
            f"Projeto: {len(source_files)} .rpy | {len(compiled_files)} compilado(s) | "
            f"compilados detectados: {compiled} | "
            + ("Problemas: " + ", ".join(issues) if issues else "estrutura válida")
        )
        self._log(self._diagnostic_summary)
        self.connectionChanged.emit()
        return not issues

    def _unren_counts(self):
        if not self._project:
            return 0, 0, 0
        game = Path(self._project) / "game"
        return (
            sum(1 for path in game.rglob("*.rpa")) if game.is_dir() else 0,
            sum(1 for path in game.rglob("*.rpyc")) if game.is_dir() else 0,
            sum(1 for path in game.rglob("*.rpymc")) if game.is_dir() else 0,
        )

    @Slot(result=str)
    def inspectUnren(self):
        if not self._project:
            self._unren_summary = "Selecione um projeto antes de usar o UnRen."
        else:
            archive_count, compiled_count, compiled_module_count = self._unren_counts()
            tool_path = Path(__file__).resolve().parents[2] / "UnRen-1.0.11d.bat"
            self._unren_summary = (
                f"UnRen: {archive_count} .rpa | {compiled_count} .rpyc | "
                f"{compiled_module_count} .rpymc | "
                + ("ferramenta encontrada." if tool_path.is_file() else "UnRen-1.0.11d.bat não encontrado.")
            )
        self._log(self._unren_summary)
        self.connectionChanged.emit()
        return self._unren_summary

    @Slot(result=bool)
    def runUnren(self):
        return self.runUnrenOption(8)

    @Slot()
    def cancelUnren(self):
        if self._unren_process is None:
            return
        self._unren_cancel_requested = True
        self._log("WARNING: cancelamento do UnRen solicitado.")
        self._unren_process.kill()

    @Slot(int, result=bool)
    def runUnrenOption(self, option):
        if option not in range(1, 9):
            self._log(f"ERROR: opção UnRen inválida: {option}")
            return False
        if not self._project or self._unren_process is not None:
            self._log("WARNING: UnRen já está em execução ou nenhum projeto foi selecionado.")
            return False
        tool_path = Path(__file__).resolve().parents[2] / "UnRen-1.0.11d.bat"
        project_root = Path(self._project)
        if not (project_root / "game").is_dir():
            self._log("ERROR: a pasta selecionada não contém a pasta game.")
            return False
        if not tool_path.is_file():
            self._log(f"ERROR: ferramenta não encontrada: {tool_path}")
            return False
        archive_count, compiled_count, compiled_module_count = self._unren_counts()
        if (
            (option == 1 and not archive_count)
            or (option == 2 and not compiled_count and not compiled_module_count)
            or (option == 8 and not archive_count and not compiled_count and not compiled_module_count)
        ):
            self._log("UnRen: nenhum .rpa/.rpyc/.rpymc encontrado.")
            return False

        backup_dir = project_root / ".alice" / "unren-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            for source in project_root.rglob("*"):
                if (
                    source.is_file()
                    and source.suffix.lower() in {".rpa", ".rpyc", ".rpymc", ".rpy"}
                    and ".alice" not in source.parts
                ):
                    target = backup_dir / source.relative_to(project_root)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
            runtime_tool = project_root / "UnRen-1.0.11d.bat"
            shutil.copy2(tool_path, runtime_tool)
            launcher_path = project_root / "alice_unren_launcher.py"
            launcher_path.write_text(
                "import runpy\n"
                "import sys\n"
                "import renpy.object\n"
                "runpy.run_path(sys.argv[1], run_name='__main__')\n",
                encoding="ascii",
            )
            batch_text = runtime_tool.read_text(encoding="utf-8")
            invocation = '"%pythondir%python.exe" -O "%unrpycpy%"'
            replacement = (
                '"%pythondir%python.exe" -O '
                '"%maindir%alice_unren_launcher.py" "%unrpycpy%"'
            )
            if invocation not in batch_text:
                raise OSError("não foi possível preparar o lançador de compatibilidade")
            runtime_tool.write_text(
                batch_text.replace(invocation, replacement),
                encoding="utf-8",
            )
            self._unren_backup_dir = backup_dir
            self._unren_option = option
            self._unren_log_path = backup_dir / "unren.log"
            self._unren_launcher_path = launcher_path
        except OSError as error:
            for temporary in (
                project_root / "UnRen-1.0.11d.bat",
                project_root / "alice_unren_launcher.py",
            ):
                try:
                    temporary.unlink(missing_ok=True)
                except OSError as cleanup_error:
                    self._log(f"WARNING: não foi possível limpar arquivo temporário: {cleanup_error}")
            self._log(f"ERROR: backup do UnRen falhou: {error}")
            return False

        command = f"call {runtime_tool.name}"
        self._unren_process = QProcess(self)
        self._unren_process.setProgram("cmd.exe")
        self._unren_process.setArguments(["/d", "/c", command])
        self._unren_process.setWorkingDirectory(str(project_root))
        self._unren_process.started.connect(self._send_unren_input)
        self._unren_process.readyReadStandardOutput.connect(self._read_unren_output)
        self._unren_process.readyReadStandardError.connect(self._read_unren_error)
        self._unren_process.finished.connect(self._unren_finished)
        self._unren_summary = f"UnRen opção {option} em execução; backup criado em {backup_dir}"
        self._unren_cancel_requested = False
        self._log(self._unren_summary)
        self.connectionChanged.emit()
        self._unren_process.start()
        self._unren_timeout_timer.start()
        return True

    def _send_unren_input(self):
        if self._unren_process is None or self._unren_option is None:
            return
        self._unren_process.write(f"{self._unren_option}\r\n\r\n".encode("ascii"))
        self._unren_process.closeWriteChannel()

    def _read_unren_output(self):
        output = bytes(self._unren_process.readAllStandardOutput()).decode(errors="replace").strip()
        if output:
            for line in output.splitlines():
                self._log(f"UnRen: {line}")
            self._append_unren_log(output)

    def _read_unren_error(self):
        output = bytes(self._unren_process.readAllStandardError()).decode(errors="replace").strip()
        if output:
            self._log(f"ERROR UnRen: {output}")
            self._append_unren_log(output)

    def _append_unren_log(self, text):
        if not self._unren_log_path:
            return
        try:
            with self._unren_log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(text + "\n")
        except OSError as error:
            self._log(f"WARNING: não foi possível salvar log do UnRen: {error}")

    @Slot(int, QProcess.ExitStatus)
    def _unren_finished(self, exit_code, _status):
        self._unren_timeout_timer.stop()
        runtime_tool = Path(self._project) / "UnRen-1.0.11d.bat"
        try:
            runtime_tool.unlink(missing_ok=True)
            if self._unren_launcher_path:
                self._unren_launcher_path.unlink(missing_ok=True)
        except OSError as error:
            self._log(f"WARNING: não foi possível remover ferramenta temporária: {error}")
        self._unren_process = None
        self.inspectUnren()
        if self._unren_cancel_requested:
            result = "cancelado"
        else:
            result = "concluído com sucesso" if exit_code == 0 else f"terminou com código {exit_code}"
        self._unren_summary = (
            f"UnRen opção {self._unren_option} {result}. "
            f"Backup: {self._unren_backup_dir}"
        )
        self._log(self._unren_summary)
        self._unren_option = None
        self.connectionChanged.emit()

    @Slot()
    def simulateTranslation(self):
        if not self.validateProject():
            return
        try:
            entries = extract_translation_entries(str(Path(self._project) / "game"))
            cache = load_cache(self._cache_path())
            cached = sum(1 for entry in entries if entry.original_text in cache)
            pending = len(entries) - cached
            self._diagnostic_summary = (
                f"Simulação: {len(entries)} entradas | "
                f"{cached} no cache | {pending} serão enviadas ao motor | "
                "nenhum arquivo foi alterado"
            )
            self._log(self._diagnostic_summary)
        except (OSError, ValueError, TypeError) as error:
            self._log(f"ERROR: falha na simulação: {error}")
        self.connectionChanged.emit()

    @Slot(int, result=str)
    def reviewOriginal(self, index):
        return self._review_originals[index] if 0 <= index < len(self._review_originals) else ""

    @Slot(int, result=str)
    def reviewTranslation(self, index):
        return self._review_translations[index] if 0 <= index < len(self._review_translations) else ""

    @Slot(str, result=int)
    def reviewIndexForDisplay(self, display_value):
        prefix = display_value
        if prefix.startswith("[REVISADA]  "):
            prefix = prefix[len("[REVISADA]  "):]
        for index, original in enumerate(self._review_originals):
            translation = self._review_translations[index]
            candidate = (
                f"[REVISADA]  {original}  →  {translation}"
                if self._review_entries[index].startswith("[REVISADA]")
                else f"[{self._review_objects[index].entry_type}]  {original}  →  {translation}"
            )
            if candidate == display_value:
                return index
        return -1

    @Slot(int, str)
    def updateReviewEntry(self, index, translation):
        if 0 <= index < len(self._review_translations):
            self._review_translations[index] = translation
            self._review_entries[index] = f"[REVISADA]  {self._review_originals[index]}  →  {translation}"
            self.reviewChanged.emit()
            self._refresh_quality()
            self._log(f"Entrada {index + 1} atualizada na revisão.")

    @Slot(int, result=bool)
    def reviewIsEdited(self, index):
        return 0 <= index < len(self._review_entries) and self._review_entries[index].startswith("[REVISADA]")

    @Slot(int, result=bool)
    def reviewIsSameAsOriginal(self, index):
        return 0 <= index < len(self._review_originals) and self._review_originals[index] == self._review_translations[index]

    @Slot(int, result=bool)
    def reviewHasIssue(self, index):
        if not 0 <= index < len(self._review_originals):
            return False
        original = self._review_originals[index]
        translated = self._review_translations[index]
        return (
            not translated
            or original == translated
            or not placeholders_match(original, translated)
            or not placeholder_spacing_matches(original, translated)
        )
    @Slot(int, result=int)
    def nextReviewIndex(self, index):
        return min(max(index + 1, 0), max(len(self._review_entries) - 1, 0))

    @Slot(int, result=int)
    def previousReviewIndex(self, index):
        return max(min(index - 1, len(self._review_entries) - 1), 0)

    @Slot()
    def saveReviewChanges(self):
        if not self._review_objects:
            self._log("Nenhuma entrada para salvar.")
            return
        try:
            cache_path = self._cache_path()
            cache = load_cache(cache_path)
            translations = {}
            for entry, translation in zip(self._review_objects, self._review_translations):
                translations[entry.translation_id] = translation
                cache[entry.original_text] = translation
            if cache_path.exists():
                backup = cache_path.with_name(f"{cache_path.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{cache_path.suffix}")
                shutil.copy2(cache_path, backup)
            save_cache(cache, cache_path)
            pipeline = TranslationPipeline(self._project, output_path="")
            output_dir = pipeline.game_path / "tl" / "portuguese"
            self._backupGeneratedFiles(output_dir)
            save_dialogue_rpy(self._review_objects, translations, "portuguese", str(output_dir / "dialogue.rpy"))
            save_strings_rpy(self._review_objects, translations, "portuguese", str(output_dir / "strings.rpy"))
            self._log("Alterações salvas e arquivos Ren'Py regenerados.")
        except Exception as error:
            self._log(f"ERROR: falha ao salvar revisão: {error}")

    def _backupGeneratedFiles(self, output_dir):
        backup_dir = output_dir / ".alice-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
        for name in ("dialogue.rpy", "strings.rpy", "zzz_alice_language.rpy"):
            source = output_dir / name
            if source.is_file():
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, backup_dir / name)
        if backup_dir.exists():
            self._log(f"Backup dos arquivos gerados criado em: {backup_dir}")

    @Slot()
    def backupGeneratedFiles(self):
        if not self._project:
            self._log("WARNING: selecione um projeto antes de criar backup.")
            return
        pipeline = TranslationPipeline(self._project, output_path="")
        self._backupGeneratedFiles(pipeline.game_path / "tl" / "portuguese")

    @Slot()
    def restoreLatestGeneratedBackup(self):
        if not self._project:
            self._log("WARNING: selecione um projeto antes de restaurar arquivos.")
            return
        output_dir = Path(self._project) / "game" / "tl" / "portuguese"
        backups = sorted((output_dir / ".alice-backups").glob("*"), reverse=True)
        if not backups:
            self._log("WARNING: nenhum backup de arquivos gerados encontrado.")
            return
        try:
            for name in ("dialogue.rpy", "strings.rpy", "zzz_alice_language.rpy"):
                source = backups[0] / name
                if source.is_file():
                    shutil.copy2(source, output_dir / name)
            self._log(f"Backup de arquivos restaurado: {backups[0]}")
        except OSError as error:
            self._log(f"ERROR: não foi possível restaurar arquivos: {error}")

    @Slot()
    def openOutputFolder(self):
        if not self._project:
            self._log("WARNING: nenhum projeto selecionado.")
            return
        output_folder = Path(self._project) / "game" / "tl" / "portuguese"
        output_folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(output_folder)))
        self._log(f"Pasta de saída aberta: {output_folder}")

    @Slot(str)
    def openGeneratedFile(self, file_path):
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(self._project) / path
        if not path.is_file():
            self._log(f"WARNING: arquivo não encontrado: {path}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        self._log(f"Arquivo aberto: {path}")

    @Slot(str)
    def copyPath(self, value):
        if value:
            QGuiApplication.clipboard().setText(value)
            self._log("Caminho copiado para a área de transferência.")

    @Slot(str, result=str)
    def exportReport(self, extension):
        suffix = ".json" if extension.lower() == "json" else ".txt"
        report_path = Path(self._project or ".") / f"alice_report{suffix}"
        report = {
            "project": self._project,
            "status": self._status,
            "progress": self._progress,
            "files": self._files,
            "entries": self._entries,
            "quality": self._quality,
            "files_generated": self._files_generated,
            "logs": self._logs,
        }
        try:
            if suffix == ".json":
                report_path.write_text(
                    json.dumps(report, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            else:
                report_path.write_text(
                    "\n".join(
                        [
                            "ALICE - RELATÓRIO",
                            f"Projeto: {self._project}",
                            f"Status: {self._status}",
                            f"Progresso: {self._progress}%",
                            f"Arquivos RPY: {self._files}",
                            f"Entradas: {self._entries}",
                            "",
                            "QUALIDADE:",
                            *self.qualitySummary,
                            "",
                            "Arquivos gerados:",
                            *self._files_generated,
                            "",
                            "LOGS:",
                            self._logs,
                        ]
                    ),
                    encoding="utf-8",
                )
        except OSError as error:
            self._log(f"ERROR: não foi possível exportar o relatório: {error}")
            return ""
        self._log(f"Relatório exportado: {report_path}")
        return str(report_path)

    @Slot(result=bool)
    def addPortugueseLanguageOption(self):
        if not self._project:
            self._log("WARNING: nenhum projeto selecionado.")
            return False
        game_path = Path(self._project) / "game"
        language_pattern = re.compile(r"^(\s*)textbutton\s+['\"]([^'\"]+)['\"]\s+action\s+Language\(")
        for source_path in sorted(game_path.rglob("*.rpy")):
            if "tl" in source_path.parts:
                continue
            lines = source_path.read_text(encoding="utf-8").splitlines(keepends=True)
            if any("Language(\"portuguese\")" in line or "Language('portuguese')" in line for line in lines):
                self._log("Português já está presente no menu de idiomas.")
                return True
            matches = [index for index, line in enumerate(lines) if "Language(" in line and "textbutton" in line]
            if not matches:
                continue
            insert_at = matches[-1] + 1
            indent = re.match(r"^\s*", lines[matches[-1]]).group(0)
            backup = source_path.with_suffix(source_path.suffix + ".alice.bak")
            if not backup.exists():
                backup.write_text("".join(lines), encoding="utf-8")
            lines.insert(insert_at, f'{indent}textbutton "Português" action Language("portuguese")\n')
            source_path.write_text("".join(lines), encoding="utf-8")
            self._log(f"Opção Português adicionada em {source_path.name}; backup criado.")
            return True
        self._log("WARNING: nenhum menu de idiomas com Language(...) foi encontrado.")
        return False

    @Slot(str, str, str, int, str, int, int)
    def saveSettings(self, source, target, engine, batch_size, api_url="", timeout=60, max_retries=3):
        self._source_language = source
        self._target_language = target
        self._engine = engine
        self._api_url = api_url.strip() or "http://localhost:5000/translate"
        self._timeout = max(1, int(timeout))
        self._max_retries = max(0, int(max_retries))
        ConfigManager().update_section("translation", {
            "source_language": source,
            "target_language": target,
            "selected_engine": engine,
            "max_batch_size": batch_size,
            "api_url": self._api_url,
            "timeout": self._timeout,
            "max_retries": self._max_retries,
        })
        self._log("Configurações de tradução salvas.")
        self.settingsChanged.emit()

    def _log(self, message):
        self._logs += f"\n[INFO] {message}"
        self.logsChanged.emit()

    @Slot(str)
    def selectProject(self, path):
        self._log(f"Validando projeto: {path}")
        root = Path(path)
        if root.name.lower() == "game":
            root = root.parent
        previous_project = self._project
        if previous_project and Path(previous_project).resolve() != root.resolve():
            self._log("Projeto alterado: usando o cache isolado do novo projeto.")
        game = root / "game"
        if not game.is_dir():
            self._project = str(root)
            self._status = "Projeto inválido: pasta game não encontrada"
            self._files = 0
            self._entries = 0
            self._log("Pasta game não encontrada.")
        else:
            self._project = str(root)
            self._status = "Projeto válido"
            self._files = sum(1 for item in game.rglob("*.rpy") if "tl" not in item.parts)
            self._entries = 0
            self._log(f"Projeto válido. {self._files} arquivo(s) .rpy encontrado(s).")

        try:
            cache_path = root / ".alice" / "cache.json"
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            ConfigManager().update_section("ui", {"last_opened_project": str(root)})
            ConfigManager().update_section("project", {
                "project_path": str(root),
                "cache_path": str(cache_path),
                "extracted_entries_path": str(root / "extracted_entries.json"),
            })
        except OSError as error:
            self._log(f"WARNING: não foi possível salvar a configuração: {error}")

        self.projectChanged.emit()
        self.statusChanged.emit()
        self.countsChanged.emit()

    @Slot()
    def startTranslation(self):
        if self._status != "Projeto válido":
            self._log("Selecione um projeto válido antes de iniciar.")
            return
        config = ConfigManager().load()
        cache_path = Path(config.project.cache_path)
        if not cache_path.is_absolute():
            cache_path = Path(__file__).resolve().parents[2] / cache_path
        try:
            invalid_entries = purge_invalid_placeholder_cache(cache_path)
        except (OSError, ValueError) as error:
            self._status = "Erro na tradução"
            self._log(f"ERROR: não foi possível validar o cache: {error}")
            self.statusChanged.emit()
            return
        if invalid_entries:
            self._log(
                f"Cache: {invalid_entries} entradas inválidas removidas para retradução."
            )
        else:
            self._log("Cache validado: nenhuma entrada inválida encontrada.")
        self._status = "Traduzindo..."
        self.backupGeneratedFiles()
        self._cancel_requested = False
        self._progress = 0
        self._files_generated = []
        self.statusChanged.emit()
        self.progressChanged.emit()
        self.filesGeneratedChanged.emit()
        self._log("Iniciando pipeline de tradução.")
        self._process = QProcess(self)
        project_root = Path(__file__).resolve().parents[2]
        self._process.setProgram(sys.executable)
        self._process.setWorkingDirectory(str(project_root))
        process_env = QProcessEnvironment.systemEnvironment()
        process_env.insert("PYTHONPATH", str(project_root))
        process_env.insert("PYTHONUNBUFFERED", "1")
        self._process.setProcessEnvironment(process_env)
        self._process.setArguments([str(project_root / "cli" / "run_cli.py"), self._project])
        self._process.readyReadStandardOutput.connect(self._read_process_output)
        self._process.readyReadStandardError.connect(self._read_process_error)
        self._process.finished.connect(self._process_finished)
        self._process.start()

    @Slot()
    def _read_process_output(self):
        output = bytes(self._process.readAllStandardOutput()).decode(errors="replace").strip()
        if output:
            for line in output.splitlines():
                self._log(line)
                self._update_progress_from_output(line)

    @Slot()
    def _read_process_error(self):
        output = bytes(self._process.readAllStandardError()).decode(errors="replace").strip()
        if output:
            self._log(f"ERROR: {output}")

    def _update_progress_from_output(self, line):
        match = re.search(r"Batch conclu[ií]do:\s*(\d+)/(\d+)", line, re.IGNORECASE)
        if not match:
            match = re.search(r"Traduzindo entrada\s+(\d+)/(\d+)", line, re.IGNORECASE)
        if not match:
            return
        current, total = (int(value) for value in match.groups())
        self._progress = min(100, max(0, int(current * 100 / total))) if total else 0
        self._status = f"Traduzindo entrada {current}/{total}"
        self.progressChanged.emit()
        self.statusChanged.emit()

    @Slot(int, QProcess.ExitStatus)
    def _process_finished(self, exit_code, exit_status):
        self._process = None
        if exit_code == 0:
            extracted = Path(self._project) / "extracted_entries.json"
            if not extracted.exists() and Path(self._project).name.lower() == "game":
                extracted = Path(self._project).parent / "extracted_entries.json"
            try:
                data = json.loads(extracted.read_text(encoding="utf-8"))
                raw_entries = data if isinstance(data, list) else data.get("entries", [])
                self._entries = len(raw_entries)
                cache = load_cache(ConfigManager().load().project.cache_path)
                self._review_objects = [TranslationEntry(**item) for item in raw_entries]
                self._review_originals = [entry.original_text for entry in self._review_objects]
                self._review_translations = [cache.get(entry.original_text, "") for entry in self._review_objects]
                self._review_entries = [
                    f"[{entry.entry_type}]  {entry.original_text}  →  {cache.get(entry.original_text, '')}"
                    for entry in self._review_objects
                ]
                self._refresh_quality()
                output_dir = Path(self._project) / "game" / "tl" / "portuguese"
                self._files_generated = [
                    str(extracted),
                    str(output_dir / "dialogue.rpy"),
                    str(output_dir / "strings.rpy"),
                    str(Path(self._project) / "game" / "zzz_alice_language.rpy"),
                ]
                self.countsChanged.emit()
                self.reviewChanged.emit()
                self.filesGeneratedChanged.emit()
                self._log(f"{self._entries} entradas carregadas do JSON.")
            except (OSError, ValueError, TypeError) as error:
                self._log(f"WARNING: não foi possível ler as entradas extraídas: {error}")
            self._progress = 100
            self._status = "Tradução concluída"
            self._history.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "project": self._project,
                "entries": self._entries,
                "translated": sum(1 for value in self._review_translations if value),
                "cache": str(self._cache_path()),
                "progress": self._progress,
                "status": "Concluída",
            })
            Path("history.json").write_text(json.dumps(self._history[:50], ensure_ascii=False, indent=2), encoding="utf-8")
            self._log("Processo externo concluído com sucesso.")
            self.progressChanged.emit()
            self.statusChanged.emit()
        else:
            self._status = "Tradução cancelada" if self._cancel_requested else "Erro na tradução"
            if not self._cancel_requested and exit_status == QProcess.CrashExit:
                self._log("ERROR: o processo de tradução foi encerrado inesperadamente.")
            self._log(self._status)
            self._cancel_requested = False
            self.statusChanged.emit()

    @Slot()
    def cancelTranslation(self):
        if self._process and self._process.state() != QProcess.NotRunning:
            self._cancel_requested = True
            self._process.terminate()
            self._status = "Cancelando tradução..."
            self._log("Solicitação de cancelamento enviada.")
            self.statusChanged.emit()
            QTimer.singleShot(3000, self._force_cancel_translation)

    def _force_cancel_translation(self):
        if self._process and self._process.state() != QProcess.NotRunning:
            self._log("O processo não encerrou após o cancelamento; finalizando.")
            self._process.kill()

    @Slot(str, int, int, str)
    def _on_progress(self, stage, current, total, message):
        self._progress = int(current * 100 / total) if total else 0
        self._status = message
        self._log(f"{stage}: {message}")
        self.progressChanged.emit()
        self.statusChanged.emit()

    @Slot(object)
    def _on_finished(self, result):
        self._progress = 100
        self._status = "Tradução concluída"
        self._files_generated = [str(path) for path in (result.output_file, result.dialogue_file, result.strings_file, result.language_file) if path]
        self._review_entries = [
            f"[{entry.entry_type}]  {entry.original_text}  →  {result.translations.get(entry.translation_id, '') if result.translations else ''}"
            for entry in result.entries
        ]
        self._review_originals = [entry.original_text for entry in result.entries]
        self._review_translations = [result.translations.get(entry.translation_id, '') if result.translations else '' for entry in result.entries]
        self._review_objects = result.entries
        self._log(f"Concluído: {len(result.entries)} entradas processadas.")
        self.progressChanged.emit()
        self.statusChanged.emit()
        self.filesGeneratedChanged.emit()
        self.reviewChanged.emit()
        self._refresh_quality()

    @Slot(str)
    def _on_failed(self, error):
        if "cancelada" in error.lower():
            self._status = "Tradução cancelada"
            self._log("Tradução cancelada pelo usuário.")
        else:
            self._status = "Erro na tradução"
            self._log(f"ERROR: {error}")
        self.statusChanged.emit()
