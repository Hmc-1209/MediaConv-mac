#!/bin/sh
mkdir MediaConv_dmg
cp -R dist/MediaConv.app MediaConv_dmg/

hdiutil create -volname "MediaConv" -srcfolder MediaConv_dmg -ov -format UDZO MediaConv.dmg

rm -rf MediaConv_dmg