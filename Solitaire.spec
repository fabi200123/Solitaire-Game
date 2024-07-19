# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['game\\game.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sprites/clubs/*.jpg', 'sprites/clubs'),
        ('sprites/cover/*.jpg', 'sprites/cover'),
        ('sprites/diamonds/*.jpg', 'sprites/diamonds'),
        ('sprites/hearts/*.jpg', 'sprites/hearts'),
        ('sprites/spades/*.jpg', 'sprites/spades')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Solitaire',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
