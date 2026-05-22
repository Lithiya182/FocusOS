import json
import os

DATA_FILE = "data/user_stats.json"

# =========================
# LOAD STATS
# =========================

def load_stats():

    if not os.path.exists(DATA_FILE):

        default_stats = {
            "focus_hours": 0,
            "completed_sessions": 0,
            "current_streak": 0,
            "focus_score": 0,
            "distractions_blocked": 0,
            "xp": 0,
            "level": 1
        }

        save_stats(default_stats)

        return default_stats

    with open(DATA_FILE, "r") as file:

        return json.load(file)

# =========================
# SAVE STATS
# =========================

def save_stats(stats):

    with open(DATA_FILE, "w") as file:

        json.dump(stats, file, indent=4)

# =========================
# ADD SESSION
# =========================

def add_completed_session(minutes):

    stats = load_stats()

    stats["completed_sessions"] += 1

    stats["focus_hours"] += round(minutes / 60, 2)

    stats["xp"] += minutes * 2

    stats["distractions_blocked"] += 3

    stats["focus_score"] = min(100, stats["focus_score"] + 5)

    stats["current_streak"] += 1

    # Level system
    stats["level"] = 1 + stats["xp"] // 200

    save_stats(stats)

    return stats