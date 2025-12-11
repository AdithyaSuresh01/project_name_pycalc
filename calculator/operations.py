from __future__ import annotations

"""Numeric operations used by the calculator.

This module defines a small operation engine that is deliberately
minimal yet easily extensible. It is used by :mod:`calculator.parser`
when evaluating parsed expressions.
"""

from dataclasses import dataclass
from typing import Callable, Dict

Number = float


@dataclass(frozen=True)
class Operation:
    """Represents a binary arithmetic operation.

    Attributes
    ----------
    symbol:
        The textual symbol for the operation, e.g. ``"+"``.
    func:
        A function implementing the operation.
    precedence:
        Operator precedence used by the expression parser.
        Higher values bind more tightly.
    associative:
        Whether the operator is left-associative (currently all are).
    """

    symbol: str
    func: Callable[[Number, Number], Number]
    precedence: int
    associative: bool = True

    def __call__(self, left: Number, right: Number) -> Number:
        """Execute the arithmetic operation."""

        return self.func(left, right)


class OperationEngine:
    """Engine that houses the supported arithmetic operations.

    The interface is intentionally small: operations are looked up by
    their symbolic representation.
    """

    def __init__(self) -> None:
        self._operations: Dict[str, Operation] = {}
        self._register_default_operations()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def _register_default_operations(self) -> None:
        """Register the standard arithmetic operations."""

        self.register("+", lambda a, b: a + b, precedence=1)
        self.register("-", lambda a, b: a - b, precedence=1)
        self.register("*", lambda a, b: a * b, precedence=2)
        self.register("/", self._safe_divide, precedence=2)
        self.register("^", lambda a, b: a ** b, precedence=3)

    @staticmethod
    def _safe_divide(a: Number, b: Number) -> Number:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def register(self, symbol: str, func: Callable[[Number, Number], Number], precedence: int,
                 associative: bool = True) -> None:
        """Register a new binary operation.

        Parameters
        ----------
        symbol:
            Single-character operator symbol.
        func:
            Callable performing the arithmetic.
        precedence:
            Operator precedence used by the parser.
        associative:
            Whether the operator is left-associative.
        """

        if not symbol or len(symbol) != 1:
            raise ValueError("Operation symbol must be a single character.")
        op = Operation(symbol=symbol, func=func, precedence=precedence, associative=associative)
        self._operations[symbol] = op

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------
    def get(self, symbol: str) -> Operation:
        """Return the :class:`Operation` for ``symbol`` or raise ``KeyError``."""

        return self._operations[symbol]

    def has(self, symbol: str) -> bool:
        """Return ``True`` if an operation with ``symbol`` is registered."""

        return symbol in self._operations

    # ------------------------------------------------------------------
    # Evaluation helper
    # ------------------------------------------------------------------
    def apply(self, symbol: str, left: Number, right: Number) -> Number:
        """Apply the operation ``symbol`` to ``left`` and ``right``.

        This is mostly a small convenience wrapper around :meth:`get`.
        """

        op = self.get(symbol)
        return op(left, right)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    @property
    def operations(self) -> Dict[str, Operation]:
        """Read-only mapping of operator symbol to :class:`Operation`."""

        return dict(self._operations)
