import time

from modules import voice_input, voice_output, reminder_manager, registry
from modules.commands import register_all


def main():
    register_all()

    voice_output.speak("Hello! I am your voice assistant.")
    print("Hello! I am your voice assistant.")
    time.sleep(0.3)

    while True:
        voice_output.speak("Listening for a command.")
        print("Listening for a command.")
        command = voice_input.listen()
        if not command:
            continue

        result = registry.dispatch(command)
        if result == registry.EXIT:
            break
        if result == registry.NOT_HANDLED:
            voice_output.speak("Sorry, I did not understand that command.")
            print("Sorry, I did not understand that command.")

        reminder_manager.check_reminders()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
