# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.api import Analysis, PYZ, EXE, COLLECT
import os

# Definiši putanju do Stockfish EXE
stockfish_exe = 'stockfish-windows-x86-64-avx2.exe'

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Putanja do trenutnog direktorijuma
    binaries=[
        (stockfish_exe, '.'),  # Uključi Stockfish EXE u binarne fajlove
    ],
    datas=[
        # Uključi sve druge potrebne datoteke ovde ako ih imaš
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Chess Bot 1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Postavi na True ako želiš da vidiš konzolu
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='chess_icon.ico',  # Ako koristiš ikonu
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Chess Bot 1.0',
)
