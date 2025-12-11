from __future__ import annotations

"""Core package for the PyCalc project.

The package exposes a small public API for programmatic use:

- :class:`calculator.operations.OperationEngine`
- :class:`calculator.parser.ExpressionParser`
- :class:`calculator.history.HistoryManager`
"""

from .operations import OperationEngine
from .parser import ExpressionParser
from .history import HistoryManager

__all__ = [
    "OperationEngine",
    "ExpressionParser",
    "HistoryManager",
]
