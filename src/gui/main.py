import os
import sys
import ctypes
from pathlib import Path

os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from src.gui.app_backend import AppBackend


def _set_windows_app_identity():
    """Dá ao processo uma identidade própria para a barra de tarefas do Windows."""
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Alice.Translator"
        )
    except (AttributeError, OSError):
        pass


def main():
    _set_windows_app_identity()
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Alice")
    icon_path = Path(__file__).with_name("assets") / "alice-icon.ico"
    app.setWindowIcon(QIcon(str(icon_path)))
    engine = QQmlApplicationEngine()
    backend = AppBackend()
    engine.rootContext().setContextProperty("appBackend", backend)
    engine.warnings.connect(lambda warnings: [print(warning.toString(), file=sys.stderr) for warning in warnings])
    engine.load(str(Path(__file__).with_name("qml") / "Main.qml"))
    if not engine.rootObjects():
        print("Falha ao carregar a interface QML.", file=sys.stderr)
        return 1
    # QQuickWindow pode não herdar o ícone global no Windows; aplicar também
    # diretamente à janela garante o ícone correto na barra de tarefas.
    engine.rootObjects()[0].setIcon(QIcon(str(icon_path)))
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
