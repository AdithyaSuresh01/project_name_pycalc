from __future__ import annotations

"""Lightweight in-memory calculation history for PyCalc."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class HistoryRecord:
    """Represents a single evaluated expression."""

    expression: str
    result: float


class HistoryManager:
    """Stores a simple ordered list of calculation records."""

    def __init__(self) -> None:
        self._records: List[HistoryRecord] = []

    def add(self, expression: str, result: float) -> None:
        """Append a new history entry."""

        self._records.append(HistoryRecord(expression=expression, result=result))

    def get_all(self) -> List[HistoryRecord]:
        """Return a copy of all stored history records."""

        return list(self._records)

    def clear(self) -> None:
        """Remove all stored history records."""

        self._records.clear()
