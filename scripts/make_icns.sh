#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/make_icns.sh <source-png> <output.icns>
# Example: scripts/make_icns.sh assets/icon.png pomodoro_py/icon.icns

SRC=${1:?"source png required"}
OUT=${2:?"output icns required"}

TMP=$(mktemp -d)
ICONSET="$TMP/icon.iconset"
mkdir -p "$ICONSET"

# sips will scale images on macOS. Create common sizes
sips -z 16 16     "$SRC" --out "$ICONSET/icon_16x16.png"
sips -z 32 32     "$SRC" --out "$ICONSET/icon_16x16@2x.png"
sips -z 32 32     "$SRC" --out "$ICONSET/icon_32x32.png"
sips -z 64 64     "$SRC" --out "$ICONSET/icon_32x32@2x.png"
sips -z 128 128   "$SRC" --out "$ICONSET/icon_128x128.png"
sips -z 256 256   "$SRC" --out "$ICONSET/icon_128x128@2x.png"
sips -z 256 256   "$SRC" --out "$ICONSET/icon_256x256.png"
sips -z 512 512   "$SRC" --out "$ICONSET/icon_256x256@2x.png"
sips -z 512 512   "$SRC" --out "$ICONSET/icon_512x512.png"
sips -z 1024 1024 "$SRC" --out "$ICONSET/icon_512x512@2x.png"

# Convert iconset to icns (macOS only)
iconutil -c icns "$ICONSET" -o "$OUT"

rm -rf "$TMP"
echo "Wrote $OUT"