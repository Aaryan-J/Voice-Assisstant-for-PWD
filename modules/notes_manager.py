import json
from .utils import get_data_path

NOTES_FILE = "notes.json"

def _load_notes():
    path = get_data_path(NOTES_FILE)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_notes(notes):
    path = get_data_path(NOTES_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

def add_note(note_text):
    notes = _load_notes()
    notes.append(note_text)
    _save_notes(notes)

def read_notes():
    return _load_notes()
