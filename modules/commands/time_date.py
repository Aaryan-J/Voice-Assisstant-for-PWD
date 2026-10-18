from datetime import datetime

from .. import registry, voice_output

_TIME_WORDS = ("time", "clock", "hour")
_DATE_WORDS = ("date",)
_DAY_WORDS = ("day", "weekday", "today")


def _speak_time(now: datetime) -> str:
    hour = now.hour % 12 or 12
    minute = now.minute
    ampm = "AM" if now.hour < 12 else "PM"
    return f"It is {hour}:{minute:02d} {ampm}."


def _speak_date(now: datetime) -> str:
    return f"Today is {now.strftime('%A, %B %d, %Y')}."


def _speak_day(now: datetime) -> str:
    return f"Today is {now.strftime('%A')}."


class TimeDateHandler(registry.Handler):
    name = "time_date"

    def match(self, command: str) -> float:
        words = command.split()
        has_time = any(w in words for w in _TIME_WORDS)
        has_date = any(w in words for w in _DATE_WORDS)
        has_day = any(w in words for w in _DAY_WORDS)
        if not (has_time or has_date or has_day):
            return 0.0
        questionish = any(
            w in words for w in ("what", "what's", "whats", "tell", "current", "now", "today")
        )
        return 0.9 if questionish else 0.5

    def run(self, command: str) -> int:
        now = datetime.now()
        words = command.split()
        if any(w in words for w in _TIME_WORDS):
            text = _speak_time(now)
        elif any(w in words for w in _DATE_WORDS):
            text = _speak_date(now)
        else:
            text = _speak_day(now)
        voice_output.speak(text)
        print(text)
        return registry.HANDLED
