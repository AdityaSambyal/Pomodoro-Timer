#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/build_mac_pyinstaller.sh [python-executable]
# Example: scripts/build_mac_pyinstaller.sh ".venv/bin/python"

PYTHON=${1:-python}
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR/pomodoro_py"

# Optional icon: use first arg or default to pomodoro_py/icon.icns
ICON=${2:-"$ROOT_DIR/assets/icon.icns"}

# If an icon source exists and is a .png, generate .icns
if [ -f "$ICON" ]; then
  ICON_ARG=(--icon "$ICON")
else
  ICON_ARG=()
fi

echo "Using Python: $("$PYTHON" --version 2>&1 | tr -d '\n')"

echo "Starting PyInstaller build..."
# Use --onedir mode for macOS .app bundles (recommended) and --windowed removes the console
"$PYTHON" -m PyInstaller --noconfirm --onedir --windowed "${ICON_ARG[@]}" --name "Pomodoro" main.py

echo "Build finished. Artifacts are under: $ROOT_DIR/pomodoro_py/dist/"
