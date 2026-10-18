HANDLED = 1
NOT_HANDLED = 0
EXIT = -1


class Handler:
    name = "base"

    def match(self, command: str) -> float:
        return 0.0

    def run(self, command: str) -> int:
        return NOT_HANDLED


_handlers: list[Handler] = []


def register(handler: Handler) -> None:
    _handlers.append(handler)


def clear() -> None:
    _handlers.clear()


def dispatch(command: str) -> int:
    best = None
    best_score = 0.0
    for h in _handlers:
        score = h.match(command)
        if score > best_score:
            best, best_score = h, score
    if best is None:
        return NOT_HANDLED
    return best.run(command)
