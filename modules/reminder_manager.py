import json
import os
from datetime import datetime
from playsound import playsound

REMINDERS_FILE = "data/reminders.json"
ALARM_FILE = "assets/alarms.mp3"

def add_reminder(reminder_text, time_str):
    reminders = []
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r") as f:
                reminders = json.load(f)
        except json.JSONDecodeError:
            reminders = []

    reminders.append({"text": reminder_text, "time": time_str})
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f)
    print("Reminder saved.")

def check_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return
    try:
        with open(REMINDERS_FILE, "r") as f:
            reminders = json.load(f)
    except json.JSONDecodeError:
        return

    now = datetime.now().strftime("%H:%M")
    for r in reminders:
        if r["time"] == now:
            print(f"Reminder: {r['text']}")
            playsound(ALARM_FILE)  # blocking
