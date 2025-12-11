# PyCalc

PyCalc is a small, educational command-line calculator written in Python.

It demonstrates a clean project layout, a tiny expression parser, and
basic unit testing with `pytest`.

## Features

- Evaluate arithmetic expressions using `+`, `-`, `*`, `/`, and `^`.
- Support for parentheses and unary minus (e.g. `-1`, `-(1+2)`).
- Simple in-memory history for interactive sessions.
- Minimal and readable codebase suitable for learning and extension.

## Installation

You can run PyCalc directly from a cloned repository or install it as a
package in editable mode.

### Clone the repository

```bash
git clone <your-repo-url> pycalc
cd pycalc
```

### Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Alternatively, if you prefer `pyproject.toml` driven installation:

```bash
pip install -e .
```

## Usage

To start the interactive calculator:

```bash
python main.py
```

You will see a prompt like:

```text
PyCalc - simple command-line calculator
Type expressions to evaluate them.
Type 'history' to show past results, 'clear' to erase history, 'quit' to exit.
> 
```

Examples:

```text
> 1 + 2 * 3
7
> (1 + 2) * 3
9
> -1 + 4
3
> -(1 + 2)
-3
> history
1: 1 + 2 * 3 = 7.0
2: (1 + 2) * 3 = 9.0
3: -1 + 4 = 3.0
4: -(1 + 2) = -3.0
> quit
Goodbye.
```

## Running tests

Tests are written using `pytest` and live in the `tests/` directory.

```bash
pytest
```

## Project layout

```text
PyCalc/
├── main.py
├── calculator/
│   ├── __init__.py
│   ├── operations.py
│   ├── history.py
│   ├── parser.py
│   └── io.py
├── tests/
│   ├── __init__.py
│   ├── test_operations.py
│   └── test_parser.py
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## Extending PyCalc

You can add new binary operations by registering them in
`OperationEngine`, for example a modulo operator:

```python
from calculator.operations import OperationEngine

engine = OperationEngine()
engine.register("%", lambda a, b: a % b, precedence=2)
```

To make the new operator usable in expressions, you only need to ensure
that the symbol is a single character; the parser will automatically
recognise it because it asks the engine which operators exist.

## License

This project is provided as-is for educational purposes. You are free to
adapt and reuse the code in your own projects.
