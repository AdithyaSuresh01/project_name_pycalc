from __future__ import annotations

"""Unit tests for :mod:`calculator.parser`."""

import math

from calculator.parser import ExpressionParser


def eval_expr(expr: str) -> float:
    return ExpressionParser().evaluate(expr)


def test_simple_addition() -> None:
    assert eval_expr("1+2") == 3


def test_addition_with_spaces() -> None:
    assert eval_expr(" 1 + 2 ") == 3


def test_precedence_multiplication_over_addition() -> None:
    assert eval_expr("1 + 2 * 3") == 7


def test_parentheses_override_precedence() -> None:
    assert eval_expr("(1 + 2) * 3") == 9


def test_nested_parentheses() -> None:
    assert eval_expr("(1 + (2 * 3))") == 7


def test_unary_minus_simple() -> None:
    assert eval_expr("-1 + 2") == 1


def test_unary_minus_with_parentheses() -> None:
    assert eval_expr("-(1 + 2)") == -3


def test_multiple_unary_minus() -> None:
    assert eval_expr("-(-1)") == 1


def test_decimal_numbers() -> None:
    assert math.isclose(eval_expr("1.5 + 2.25"), 3.75)


def test_division() -> None:
    assert eval_expr("8 / 4") == 2


def test_power_operator_precedence() -> None:
    assert eval_expr("2 ^ 3 * 2") == 16


def test_invalid_character_raises() -> None:
    try:
        eval_expr("1 + a")
    except ValueError as exc:
        assert "Unexpected character" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError")


def test_mismatched_parentheses_raises() -> None:
    try:
        eval_expr("(1 + 2")
    except ValueError as exc:
        assert "Mismatched parentheses" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError")


def test_insufficient_values_raises() -> None:
    parser = ExpressionParser()
    try:
        parser._eval_rpn([])  # type: ignore[attr-defined]
    except ValueError as exc:
        assert "Invalid expression" in str(exc) or "Insufficient values" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError")
