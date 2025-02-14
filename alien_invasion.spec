# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['alien_invasion.py','alien.py','bullet.py','button.py','game_stats.py','scoreboard.py','settings.py','ship.py'],
    pathex=[],
    binaries=[('images','images')],
    datas=[],
    hiddenimports=[],
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
    name='alien_invasion',
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
app = BUNDLE(
    exe,
    name='alien_invasion.app',
    icon=None,
    bundle_identifier=None,
)
