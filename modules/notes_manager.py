import json
import os

NOTES_FILE = "data/notes.json"

def add_note(note_text):
    notes = []
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        except json.JSONDecodeError:
            notes = []
    notes.append(note_text)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)
    print("Note saved.")

def read_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
            return notes
        except json.JSONDecodeError:
            return []
    return []
