import calendar
import re
from datetime import datetime, timedelta

_WEEKDAYS = [
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
]

_MONTHS: dict[str, int] = {}
for _i in range(1, 13):
    _name = calendar.month_name[_i].lower()
    _MONTHS[_name] = _i
    _MONTHS[_name[:3]] = _i


def _to24(hour: int, meridiem: str | None) -> int | None:
    if meridiem == "pm" and hour != 12:
        hour += 12
    elif meridiem == "am" and hour == 12:
        hour = 0
    if 0 <= hour <= 23:
        return hour
    return None


def parse_time(text: str) -> str | None:
    t = text.lower().strip()
    if "noon" in t:
        return "12:00"
    if "midnight" in t:
        return "00:00"

    m = re.search(r"\b(\d{1,2}):(\d{2})\s*(am|pm)?\b", t)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2))
        hour24 = _to24(hour, m.group(3))
        if hour24 is not None and 0 <= minute <= 59:
            return f"{hour24:02d}:{minute:02d}"

    m = re.search(r"\b(\d{1,2})\s*(am|pm)\b", t)
    if m:
        hour24 = _to24(int(m.group(1)), m.group(2))
        if hour24 is not None:
            return f"{hour24:02d}:00"

    return None


def parse_date(text: str) -> str | None:
    t = text.lower().strip()
    today = datetime.now().date()

    if "today" in t or "tonight" in t:
        return today.strftime("%Y-%m-%d")
    if "tomorrow" in t or re.search(r"\btmr\b", t):
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    if "next week" in t:
        return (today + timedelta(days=7)).strftime("%Y-%m-%d")

    for i, wd in enumerate(_WEEKDAYS):
        if wd in t:
            days_ahead = (i - today.weekday()) % 7
            if "next" in t and days_ahead == 0:
                days_ahead = 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    m = re.search(r"\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\b", t)
    if m and m.group(1) in _MONTHS:
        month = _MONTHS[m.group(1)]
        day = int(m.group(2))
        for year in (today.year, today.year + 1):
            try:
                candidate = datetime(year, month, day).date()
            except ValueError:
                return None
            if candidate >= today:
                return candidate.strftime("%Y-%m-%d")
        return None

    return None


def parse_when(text: str) -> tuple[str | None, str | None]:
    return parse_date(text), parse_time(text)


def describe_time(time_str: str) -> str:
    hour, minute = map(int, time_str.split(":"))
    meridiem = "AM" if hour < 12 else "PM"
    hour12 = hour % 12 or 12
    return f"{hour12}:{minute:02d} {meridiem}"


def describe_date(date_str: str) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    if d == today:
        return "today"
    if d == today + timedelta(days=1):
        return "tomorrow"
    return d.strftime("%A, %B %d")
