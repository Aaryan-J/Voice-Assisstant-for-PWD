from .. import registry, voice_output, voice_input, notes_manager


class NotesHandler(registry.Handler):
    name = "notes"

    def match(self, command: str) -> float:
        if "note" not in command:
            return 0.0
        if "make" in command or "add" in command or "write" in command:
            return 0.9
        if "read" in command or "show" in command or "list" in command:
            return 0.9
        return 0.0

    def run(self, command: str) -> int:
        if any(w in command for w in ("read", "show", "list")):
            return self._read_notes()
        return self._make_note()

    def _make_note(self) -> int:
        voice_output.speak("What should I write in your note?")
        print("What should I write in your note?")
        note_text = voice_input.listen()
        if note_text:
            notes_manager.add_note(note_text)
            voice_output.speak("Note saved.")
            print(f"Note saved: {note_text}")
        else:
            voice_output.speak("I did not catch that. Note not saved.")
            print("I did not catch that. Note not saved.")
        return registry.HANDLED

    def _read_notes(self) -> int:
        notes = notes_manager.read_notes()
        notes = [n for n in notes if n.lower() not in ("exit", "stop", "quit")]
        notes = list(dict.fromkeys(notes))

        if notes:
            voice_output.speak("Here are your notes:")
            for n in notes:
                print(f"Speaking note: {n}")
                voice_output.speak(n)
        else:
            voice_output.speak("You have no notes.")
        return registry.HANDLED
