import json, os, tkinter as tk
from tkinter import messagebox

APP_NAME = "ShowClicks"

BASE = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", APP_NAME)
FILE = os.path.join(BASE, "settings.json")

os.makedirs(BASE, exist_ok=True)

default = {
    "size": 100,
    "speed": 0.02,
    "thick": 3,
    "enabled": True,

    "circle_enabled": True,
    "circle_color": "yellow",
    "circle_size": 30,
    "circle_alpha": 0.7,

    "autostart": False,

    "colors": {
        "left": "white",
        "right": "red",
        "middle": "blue"
    }
}

def _popup(msg):
    try:
        r = tk.Tk()
        r.withdraw()
        messagebox.showerror("ShowClicks Error", msg)
        r.destroy()
    except:
        pass

def load():
    if not os.path.exists(FILE):
        save(default.copy())
        return default.copy()
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
        for k in default:
            if k not in data:
                data[k] = default[k]
        return data
    except:
        _popup("Settings file is corrupted.\nResetting to defaults.")
        save(default.copy())
        return default.copy()

def save(data):
    try:
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)
    except:
        _popup("Failed to save settings.\nCheck permissions or disk space.")