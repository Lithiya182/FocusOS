import json
import os

CONFIG_FILE = "data/config.json"

DEFAULT_CONFIG = {

    "productive_apps": [
        "code.exe",
        "pycharm64.exe"
    ],

    "distracting_apps": [
        "discord.exe",
        "spotify.exe",
        "vlc.exe"
    ],

    "productive_sites": [
        "github.com",
        "chatgpt.com"
    ],

    "distracting_sites": [
        "youtube.com",
        "instagram.com"
    ]
}

# =========================
# LOAD CONFIG
# =========================

def load_config():

    if not os.path.exists(CONFIG_FILE):

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as file:

        return json.load(file)

# =========================
# SAVE CONFIG
# =========================

def save_config(config):

    with open(CONFIG_FILE, "w") as file:

        json.dump(config, file, indent=4)