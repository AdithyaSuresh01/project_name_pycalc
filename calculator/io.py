from __future__ import annotations

"""Input/output helpers for PyCalc.

Currently this exposes a console-based IO abstraction which is simple
but keeps user interaction decoupled from the rest of the logic.
"""

from typing import Optional


class ConsoleIO:
    """Simple console IO wrapper.

    Abstracting I/O makes it easier to test components that depend on
    user interaction in the future, if desired.
    """

    def read_line(self, prompt: str = "") -> Optional[str]:
        """Read a line from standard input.

        Parameters
        ----------
        prompt:
            String presented to the user before reading.
        """

        return input(prompt)

    def write_line(self, text: str) -> None:
        """Write a line to standard output."""

        print(text)
