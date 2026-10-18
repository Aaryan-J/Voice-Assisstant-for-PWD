from .. import registry, voice_output

_WORDS = ("exit", "stop", "quit")


class ExitHandler(registry.Handler):
    name = "exit"

    def match(self, command: str) -> float:
        words = command.split()
        if any(w in words for w in _WORDS):
            return 0.95
        return 0.0

    def run(self, command: str) -> int:
        voice_output.speak("Goodbye!")
        print("Goodbye!")
        return registry.EXIT
