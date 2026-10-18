from .. import registry, voice_output, voice_input, reminder_manager
from ..datetime_parse import describe_date, describe_time, parse_when


def _describe_when(date_str, time_str) -> str:
    parts = []
    if date_str:
        parts.append(describe_date(date_str))
    if time_str:
        parts.append(describe_time(time_str))
    return " ".join(parts) if parts else "an unspecified time"


class RemindersHandler(registry.Handler):
    name = "reminders"

    def match(self, command: str) -> float:
        if "reminder" in command or "alarm" in command or "remind" in command:
            return 0.9
        return 0.0

    def run(self, command: str) -> int:
        voice_output.speak("What is the reminder?")
        print("What is the reminder?")
        reminder_text = voice_input.listen()
        if not reminder_text:
            voice_output.speak("I did not catch that. Reminder not saved.")
            print("I did not catch that. Reminder not saved.")
            return registry.HANDLED

        voice_output.speak(
            "When should I remind you? For example, tomorrow at 3 PM, "
            "Monday at 9 AM, or just 3 PM for today."
        )
        print("When should I remind you?")
        when_text = voice_input.listen()
        if not when_text:
            voice_output.speak("I did not catch when. Reminder not saved.")
            print("I did not catch when. Reminder not saved.")
            return registry.HANDLED

        date_str, time_str = parse_when(when_text)
        if not time_str:
            voice_output.speak("I did not catch a valid time. Reminder not saved.")
            print("I did not catch a valid time. Reminder not saved.")
            return registry.HANDLED

        reminder_manager.add_reminder(reminder_text, time_str, date_str)
        confirmation = (
            f"Reminder saved: {reminder_text}, {_describe_when(date_str, time_str)}."
        )
        voice_output.speak(confirmation)
        print(confirmation)
        return registry.HANDLED
