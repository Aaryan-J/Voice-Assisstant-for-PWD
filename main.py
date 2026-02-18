import time
from modules import voice_input, voice_output, notes_manager, reminder_manager
from datetime import datetime

def main():
    voice_output.speak("Hello! I am your voice assistant.")
    print("Hello! I am your voice assistant.")
    time.sleep(0.3)

    while True:
        voice_output.speak("Listening for a command.")
        print("Listening for a command.")
        command = voice_input.listen()
        if not command:
            continue
        command = command.lower().strip()

        # --- MAKE NOTES ---
        if "note" in command and ("make" in command or "add" in command):
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

        # --- READ NOTES ---
        elif "note" in command and ("read" in command or "show" in command):
            notes = notes_manager.read_notes()
            # filter duplicates and system keywords
            notes = [n for n in notes if n.lower() not in ["exit", "stop", "quit"]]
            notes = list(dict.fromkeys(notes))

            if notes:
                voice_output.speak("Here are your notes:")
                for n in notes:
                    print(f"Speaking note: {n}")
                    voice_output.speak(n)
            else:
                voice_output.speak("You have no notes.")

        # --- REMINDERS ---
        elif "reminder" in command or "alarm" in command:
            voice_output.speak("What is the reminder?")
            print("What is the reminder?")
            reminder_text = voice_input.listen()
            voice_output.speak("At what time? Please say in HH:MM format.")
            print("At what time? Please say in HH:MM format.")
            time_text = voice_input.listen()
            reminder_manager.add_reminder(reminder_text, time_text)
            voice_output.speak("Reminder saved.")
            print("Reminder saved.")

        # --- EXIT ---
        elif any(word in command for word in ["exit", "stop", "quit"]):
            voice_output.speak("Goodbye!")
            print("Goodbye!")
            break

        # --- UNKNOWN COMMAND ---
        else:
            voice_output.speak("Sorry, I did not understand that command.")
            print("Sorry, I did not understand that command.")

        # --- CHECK REMINDERS ---
        reminder_manager.check_reminders()
        time.sleep(0.5)

if __name__ == "__main__":
    main()
