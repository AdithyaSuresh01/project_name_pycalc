from __future__ import annotations

"""Unit tests for :mod:`calculator.operations`."""

import math

from calculator.operations import OperationEngine


def test_default_operations_exist() -> None:
    engine = OperationEngine()
    for symbol in "+-*/^":
        assert engine.has(symbol)


def test_addition() -> None:
    engine = OperationEngine()
    assert engine.apply("+", 1, 2) == 3


def test_subtraction() -> None:
    engine = OperationEngine()
    assert engine.apply("-", 5, 3) == 2


def test_multiplication() -> None:
    engine = OperationEngine()
    assert engine.apply("*", 4, 3) == 12


def test_division() -> None:
    engine = OperationEngine()
    assert engine.apply("/", 8, 2) == 4


def test_division_by_zero() -> None:
    engine = OperationEngine()
    try:
        engine.apply("/", 1, 0)
    except ZeroDivisionError:
        pass
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ZeroDivisionError")


def test_power() -> None:
    engine = OperationEngine()
    assert engine.apply("^", 2, 3) == 8


def test_custom_operation_registration() -> None:
    engine = OperationEngine()
    engine.register("%", lambda a, b: a % b, precedence=2)
    assert engine.apply("%", 10, 3) == 1


def test_operations_are_pure() -> None:
    engine = OperationEngine()
    result1 = engine.apply("+", 1, 2)
    result2 = engine.apply("+", 1, 2)
    assert result1 == result2 == 3


def test_power_non_integer_exponent() -> None:
    engine = OperationEngine()
    result = engine.apply("^", 9, 0.5)
    assert math.isclose(result, 3.0)
