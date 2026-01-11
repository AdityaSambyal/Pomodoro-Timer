#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/create_dmg.sh <path-to-app> <output-dmg>
# Example: scripts/create_dmg.sh pomodoro_py/dist/Pomodoro.app pomodoro-1.0.0.dmg

APP_PATH=${1:?"app path required"}
OUT_DMG=${2:?"output dmg required"}

DIR=$(mktemp -d)
cp -R "$APP_PATH" "$DIR/"
hdiutil create -volname "Pomodoro" -srcfolder "$DIR" -ov -format UDZO "$OUT_DMG"
rm -rf "$DIR"

echo "Created $OUT_DMG"