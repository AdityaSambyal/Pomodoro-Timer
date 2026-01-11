# Pomodoro (Python Desktop)

A small cross-platform Pomodoro desktop app built with PySide6.

## Quickstart

1. Create a virtual environment and activate it:

   python -m venv .venv
   source .venv/bin/activate

2. Install requirements:

   pip install -r requirements.txt

3. Run:

   python main.py

Notes:
- Notifications use `plyer` and behavior varies by platform; on macOS you may need to allow notifications for your Python interpreter.
- Sound: application uses `simpleaudio` to play a completion tone. It's included in `requirements.txt`.
- Haptics: on macOS you can optionally install `pyobjc-framework-AppKit` (`pip install pyobjc-framework-AppKit`) to enable hardware haptics; otherwise the app falls back to a short sound.
- To package: use PyInstaller (e.g., `pyinstaller --onefile main.py`) or Briefcase for native bundles.
