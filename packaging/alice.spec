# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


project_root = Path(SPECPATH).parent
datas = [
    (str(project_root / "src" / "gui" / "qml"), "qml"),
    (str(project_root / "src" / "gui" / "assets"), "assets"),
    (str(project_root / "UnRen-1.0.11d.bat"), "."),
]

a = Analysis(
    [str(project_root / "src" / "gui" / "main.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules("unrpa"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Alice",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(project_root / "src" / "gui" / "assets" / "alice-icon.ico"),
)
