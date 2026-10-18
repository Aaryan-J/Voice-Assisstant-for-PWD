import re
import time

from modules import voice_input, voice_output, reminder_manager, registry
from modules.commands import register_all


def _normalize(command: str) -> str:
    command = command.lower().strip()
    command = re.sub(r"[.!?;,]+$", "", command)
    command = re.sub(r"^[.!?;,]+", "", command)
    command = re.sub(r"[^0-9a-z+\-*/%.: ]", " ", command)
    return re.sub(r"\s+", " ", command).strip()


def main():
    register_all()

    voice_output.speak("Hello! I am your voice assistant.")
    print("Hello! I am your voice assistant.")
    time.sleep(0.3)

    while True:
        reminder_manager.check_reminders()

        voice_output.speak("Listening for a command.")
        print("Listening for a command.")
        command = voice_input.listen()
        if not command:
            time.sleep(0.5)
            continue
        command = _normalize(command)

        result = registry.dispatch(command)
        if result == registry.EXIT:
            break
        if result == registry.NOT_HANDLED:
            voice_output.speak("Sorry, I did not understand that command.")
            print("Sorry, I did not understand that command.")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
