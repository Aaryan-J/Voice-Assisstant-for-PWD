from .. import registry
from .calculator import CalculatorHandler
from .exit_cmd import ExitHandler
from .notes import NotesHandler
from .reminders import RemindersHandler
from .time_date import TimeDateHandler


def register_all() -> None:
    registry.register(ExitHandler())
    registry.register(NotesHandler())
    registry.register(RemindersHandler())
    registry.register(TimeDateHandler())
    registry.register(CalculatorHandler())
