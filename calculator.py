import re
import math


SAFE_NAMES = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "log": math.log, "log10": math.log10,
    "pi": math.pi, "e": math.e,
}


def calculate(expression):
    expr = expression.strip().rstrip("=").strip()
    if not re.fullmatch(r"[\d\s\+\-\*/\.\(\)\^a-zA-Z]+", expr):
        raise ValueError("Invalid characters in expression")
    expr = expr.replace("^", "**")
    # Replace imaginary `i` (not part of a function name) with Python's `j`
    expr = re.sub(r"(?<![a-zA-Z])(\d*)i(?![a-zA-Z])", lambda m: (m.group(1) or "1") + "j", expr)
    result = eval(expr, {"__builtins__": {}}, SAFE_NAMES)
    if isinstance(result, complex):
        return str(result).replace("j", "i")
    return result


def main():
    print("Calculator (type 'quit' to exit)")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if line.lower() in ("quit", "exit"):
            break
        if not line:
            continue
        if not line.endswith("="):
            print("Error: expression must end with '='")
            continue

        try:
            result = calculate(line)
            print(result)
        except ZeroDivisionError:
            print("Error: division by zero")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
