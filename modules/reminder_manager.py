import json
import wave
from datetime import datetime
import numpy as np
import sounddevice as sd
from .utils import get_data_path, get_asset_path

REMINDERS_FILE = "reminders.json"
ALARM_FILE = "alarms.wav"

def _load_reminders():
    path = get_data_path(REMINDERS_FILE)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_reminders(reminders):
    path = get_data_path(REMINDERS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(reminder_text, time_str):
    reminders = _load_reminders()
    reminders.append({"text": reminder_text, "time": time_str})
    _save_reminders(reminders)

def _play_alarm():
    alarm_path = get_asset_path(ALARM_FILE)
    if not alarm_path.exists():
        return
    try:
        with wave.open(str(alarm_path), "rb") as wf:
            if wf.getsampwidth() != 2:
                print(f"Warning: {ALARM_FILE} is not 16-bit audio, skipping alarm.")
                return
            if wf.getnchannels() != 1:
                print(f"Warning: {ALARM_FILE} is not mono, skipping alarm.")
                return
            frames = wf.readframes(wf.getnframes())
            rate = wf.getframerate()
            audio_np = np.frombuffer(frames, dtype=np.int16)
        sd.play(audio_np, samplerate=rate)
        sd.wait()
    except Exception as e:
        print(f"Error playing alarm: {e}")

def check_reminders():
    reminders = _load_reminders()
    if not reminders:
        return

    now = datetime.now().strftime("%H:%M")
    triggered = [r for r in reminders if r["time"] == now]
    if not triggered:
        return

    remaining = [r for r in reminders if r["time"] != now]
    _save_reminders(remaining)

    for r in triggered:
        print(f"Reminder: {r['text']}")

    _play_alarm()
