# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui/gui.py'],
    pathex=[],
    binaries=[('core/build/libvideo_converter.dylib', 'core/build'), ('core/build/libimage_converter.dylib', 'core/build')],
    datas=[('bin/ffmpeg', 'bin')],
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
    name='MediaConv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/app_icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MediaConv',
)
app = BUNDLE(
    coll,
    name='MediaConv.app',
    icon='icons/app_icon.icns',
    bundle_identifier=None,
)
