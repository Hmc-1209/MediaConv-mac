#!/bin/sh

pyinstaller --noconsole --onedir \
    --name MediaConv \
    --icon=icons/app_icon.icns \
    --add-binary "core/build/libvideo_converter.dylib:core/build" \
    --add-binary "core/build/libimage_converter.dylib:core/build" \
    --add-data "bin/ffmpeg:bin" \
    gui/gui.py
chmod +x dist/MediaConv/_internal/bin/ffmpeg