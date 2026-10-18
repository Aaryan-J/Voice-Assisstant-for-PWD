import ast
import operator
import re

from .. import registry, voice_output

_ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9,
}
_TEENS = {
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
_NUMBER_WORDS = set(_ONES) | set(_TEENS) | set(_TENS) | {"hundred", "thousand"}

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FILLER = re.compile(
    r"\b(what\s+is|what's|whats|calculate|compute|work out|the result of|equals?|please|solve)\b"
)

_WORD_OPS = [
    ("to the power of", "**"),
    ("multiplied by", "*"),
    ("divided by", "/"),
    ("times", "*"),
    ("plus", "+"),
    ("minus", "-"),
    ("over", "/"),
    ("squared", "** 2"),
    ("cubed", "** 3"),
]

_OPERATOR_WORDS = (
    "plus", "minus", "times", "multiplied", "divided", "over", "power", "squared", "cubed",
)
_REQUEST_WORDS = ("calculate", "compute", "solve", "work")


def _parse_number_run(words: list[str]) -> int:
    total = 0
    current = 0
    for w in words:
        if w in _ONES:
            current += _ONES[w]
        elif w in _TEENS:
            current += _TEENS[w]
        elif w in _TENS:
            current += _TENS[w]
        elif w == "hundred":
            current = (current or 1) * 100
        elif w == "thousand":
            total += (current or 1) * 1000
            current = 0
    return total + current


def number_words_to_digits(expr: str) -> str:
    tokens = expr.split()
    out: list[str] = []
    i = 0
    while i < len(tokens):
        if tokens[i] in _NUMBER_WORDS:
            j = i
            while j < len(tokens) and tokens[j] in _NUMBER_WORDS:
                j += 1
            out.append(str(_parse_number_run(tokens[i:j])))
            i = j
        else:
            out.append(tokens[i])
            i += 1
    return " ".join(out)


def _to_expression(command: str) -> str:
    text = command.lower().strip()
    text = _FILLER.sub(" ", text)
    for word, sym in _WORD_OPS:
        text = re.sub(rf"\b{re.escape(word)}\b", f" {sym} ", text)
    text = re.sub(r"[^0-9a-z+\-*/%. ]", " ", text)
    text = number_words_to_digits(text)
    return re.sub(r"\s+", " ", text).strip()


def _safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError(f"unsupported expression: {ast.dump(node)}")

    return _eval(ast.parse(expr, mode="eval"))


def _format_result(value: float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def try_calculate(command: str) -> str | None:
    expr = _to_expression(command)
    if not expr or not re.search(r"\d", expr):
        return None
    if not re.search(r"[+\-*/%]", expr):
        return None
    try:
        result = _safe_eval(expr)
    except ZeroDivisionError:
        return "You cannot divide by zero."
    except Exception:
        return None
    return f"{_format_result(result)}."


class CalculatorHandler(registry.Handler):
    name = "calculator"

    def match(self, command: str) -> float:
        words = command.split()
        has_number = any(ch.isdigit() for ch in command) or any(
            w in _NUMBER_WORDS for w in words
        )
        has_operator = any(w in words for w in _OPERATOR_WORDS)
        is_request = any(w in words for w in _REQUEST_WORDS) or "what" in words
        if has_number and (has_operator or (is_request and has_number)):
            return 0.85
        return 0.0

    def run(self, command: str) -> int:
        answer = try_calculate(command)
        if answer is None:
            voice_output.speak("Sorry, I could not calculate that.")
            print("Sorry, I could not calculate that.")
            return registry.HANDLED
        voice_output.speak(answer)
        print(answer)
        return registry.HANDLED
