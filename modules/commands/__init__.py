from .. import registry
from .calculator import CalculatorHandler
from .exit_cmd import ExitHandler
from .help_cmd import HelpHandler
from .notes import NotesHandler
from .reminders import RemindersHandler
from .time_date import TimeDateHandler


def register_all() -> None:
    registry.clear()
    registry.register(ExitHandler())
    registry.register(HelpHandler())
    registry.register(NotesHandler())
    registry.register(RemindersHandler())
    registry.register(TimeDateHandler())
    registry.register(CalculatorHandler())
