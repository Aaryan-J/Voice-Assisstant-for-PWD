from .. import registry, voice_output

_HELP_WORDS = ("help", "what can you do", "commands", "options")


class HelpHandler(registry.Handler):
    name = "help"

    def match(self, command: str) -> float:
        if "help" in command:
            return 0.95
        # also handle "what can you do"
        if any(w in command for w in ("what can you", "commands", "show commands")):
            return 0.9
        return 0.0

    def run(self, command: str) -> int:
        help_text = (
            "I can help you with notes, reminders, time and date, calculator, and exit. "
            "Say 'make a note', 'read notes', 'set reminder for tomorrow at 3 PM', "
            "'what time is it', 'what is 42 times 7', or 'exit'."
        )
        voice_output.speak(help_text)
        print(help_text)
        return registry.HANDLED
