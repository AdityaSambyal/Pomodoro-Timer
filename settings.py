import os
import json

def settings_path():
    home = os.path.expanduser("~")
    p = os.path.join(home, ".pomodoro_settings.json")
    return p

def load_settings():
    try:
        with open(settings_path(), "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(d):
    try:
        cur = load_settings()
        cur.update(d)
        with open(settings_path(), "w") as f:
            json.dump(cur, f, indent=2)
    except Exception as e:
        print("Failed saving settings:", e)
