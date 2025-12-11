from __future__ import annotations

"""Entry point for the PyCalc CLI application.

This module wires together the calculator components and exposes
an interactive command-line interface.
"""

from calculator.io import ConsoleIO
from calculator.parser import ExpressionParser
from calculator.operations import OperationEngine
from calculator.history import HistoryManager


def run() -> None:
    """Run the interactive PyCalc REPL.

    Commands:
    - arithmetic expressions, e.g. `1 + 2 * 3`
    - `history` to show previous calculations
    - `clear` to clear calculation history
    - `quit` / `exit` to terminate the program
    """

    io = ConsoleIO()
    engine = OperationEngine()
    history = HistoryManager()
    parser = ExpressionParser(engine)

    io.write_line("PyCalc - simple command-line calculator")
    io.write_line("Type expressions to evaluate them.")
    io.write_line("Type 'history' to show past results, 'clear' to erase history, 'quit' to exit.\n")

    while True:
        try:
            line = io.read_line(prompt="> ")
        except (EOFError, KeyboardInterrupt):
            io.write_line("\nExiting PyCalc.")
            break

        if line is None:
            # Should not happen for console IO but keeps API generic
            continue

        stripped = line.strip()
        if not stripped:
            continue

        # REPL meta-commands
        lower = stripped.lower()
        if lower in {"quit", "exit"}:
            io.write_line("Goodbye.")
            break
        if lower == "history":
            records = history.get_all()
            if not records:
                io.write_line("(no history)")
            else:
                for idx, record in enumerate(records, start=1):
                    io.write_line(f"{idx}: {record.expression} = {record.result}")
            continue
        if lower == "clear":
            history.clear()
            io.write_line("History cleared.")
            continue

        # Expression evaluation
        try:
            result = parser.evaluate(stripped)
            history.add(stripped, result)
            io.write_line(str(result))
        except Exception as exc:  # noqa: BLE001 - user-facing REPL
            io.write_line(f"Error: {exc}")


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    run()
