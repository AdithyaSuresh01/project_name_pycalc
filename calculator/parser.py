from __future__ import annotations

"""Expression parser and evaluator for PyCalc.

The parser implements a small expression grammar supporting:

- binary operations: ``+``, ``-``, ``*``, ``/``, ``^``
- unary minus (e.g. ``-2`` or ``-(1 + 2)``)
- parentheses
- floating point numbers.

It uses a variant of Dijkstra's *shunting-yard* algorithm to convert
infix expressions into Reverse Polish Notation (RPN), which is then
evaluated using the :class:`calculator.operations.OperationEngine`.
"""

from dataclasses import dataclass
from typing import List, Union

from .operations import OperationEngine, Number


@dataclass(frozen=True)
class NumberToken:
    value: Number


@dataclass(frozen=True)
class OperatorToken:
    symbol: str


@dataclass(frozen=True)
class LeftParenToken:
    pass


@dataclass(frozen=True)
class RightParenToken:
    pass


Token = Union[NumberToken, OperatorToken, LeftParenToken, RightParenToken]


class ExpressionParser:
    """Parse and evaluate simple arithmetic expressions."""

    def __init__(self, engine: OperationEngine | None = None) -> None:
        self.engine = engine or OperationEngine()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def evaluate(self, expression: str) -> Number:
        """Parse and evaluate ``expression``.

        Parameters
        ----------
        expression:
            Infix arithmetic expression.
        """

        tokens = self._tokenise(expression)
        rpn = self._to_rpn(tokens)
        return self._eval_rpn(rpn)

    # ------------------------------------------------------------------
    # Tokenisation
    # ------------------------------------------------------------------
    def _tokenise(self, expression: str) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        n = len(expression)
        last_token: Token | None = None

        while i < n:
            ch = expression[i]

            if ch.isspace():
                i += 1
                continue

            # Number literal (supports simple floats)
            if ch.isdigit() or (ch == "." and i + 1 < n and expression[i + 1].isdigit()):
                start = i
                has_dot = ch == "."
                i += 1
                while i < n:
                    c = expression[i]
                    if c.isdigit():
                        i += 1
                        continue
                    if c == "." and not has_dot:
                        has_dot = True
                        i += 1
                        continue
                    break
                tokens.append(NumberToken(float(expression[start:i])))
                last_token = tokens[-1]
                continue

            # Parentheses
            if ch == "(":
                tokens.append(LeftParenToken())
                last_token = tokens[-1]
                i += 1
                continue
            if ch == ")":
                tokens.append(RightParenToken())
                last_token = tokens[-1]
                i += 1
                continue

            # Operators, including unary minus handled during RPN conversion
            if self.engine.has(ch):
                tokens.append(OperatorToken(ch))
                last_token = tokens[-1]
                i += 1
                continue

            raise ValueError(f"Unexpected character at position {i}: '{ch}'")

        return tokens

    # ------------------------------------------------------------------
    # Shunting-yard to RPN
    # ------------------------------------------------------------------
    def _to_rpn(self, tokens: List[Token]) -> List[Token]:
        output: List[Token] = []
        ops: List[OperatorToken | LeftParenToken] = []
        prev: Token | None = None

        for token in tokens:
            if isinstance(token, NumberToken):
                output.append(token)
                prev = token
                continue

            if isinstance(token, OperatorToken):
                # Detect unary minus and convert "-x" to "0 - x" pattern
                if token.symbol == "-" and (
                    prev is None
                    or isinstance(prev, OperatorToken)
                    or isinstance(prev, LeftParenToken)
                ):
                    # Insert an implicit zero before unary minus
                    output.append(NumberToken(0.0))

                # Pop operators from stack based on precedence
                while ops and isinstance(ops[-1], OperatorToken):
                    top = ops[-1]
                    top_op = self.engine.get(top.symbol)
                    cur_op = self.engine.get(token.symbol)
                    if top_op.precedence >= cur_op.precedence:
                        output.append(ops.pop())
                    else:
                        break
                ops.append(token)
                prev = token
                continue

            if isinstance(token, LeftParenToken):
                ops.append(token)
                prev = token
                continue

            if isinstance(token, RightParenToken):
                # Pop until matching left parenthesis found
                while ops and not isinstance(ops[-1], LeftParenToken):
                    output.append(ops.pop())
                if not ops or not isinstance(ops[-1], LeftParenToken):
                    raise ValueError("Mismatched parentheses")
                ops.pop()  # discard left paren
                prev = token
                continue

        # Drain remaining operators
        while ops:
            op = ops.pop()
            if isinstance(op, LeftParenToken):
                raise ValueError("Mismatched parentheses")
            output.append(op)

        return output

    # ------------------------------------------------------------------
    # RPN evaluation
    # ------------------------------------------------------------------
    def _eval_rpn(self, tokens: List[Token]) -> Number:
        stack: List[Number] = []

        for token in tokens:
            if isinstance(token, NumberToken):
                stack.append(token.value)
                continue

            if isinstance(token, OperatorToken):
                if len(stack) < 2:
                    raise ValueError("Insufficient values in expression")
                b = stack.pop()
                a = stack.pop()
                res = self.engine.apply(token.symbol, a, b)
                stack.append(res)
                continue

            raise ValueError("Invalid token in RPN expression")

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack
