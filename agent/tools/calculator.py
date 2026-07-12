"""
agent/tools/calculator.py — Herramienta de cálculo matemático.

La evaluación se realiza con un parser AST seguro que solo permite
expresiones aritméticas básicas con números y operadores +, -, *, /, **.
"""

import ast
from typing import Any


class SafeExpressionError(ValueError):
    """Se lanza cuando la expresión contiene elementos no permitidos."""


def _evaluate_node(node: ast.AST) -> Any:
    """Evalua de forma segura un nodo del AST de una expresión aritmética."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise SafeExpressionError("solo se permiten números")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand)
        if not isinstance(operand, (int, float)) or isinstance(operand, bool):
            raise SafeExpressionError("operando no numérico")
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise SafeExpressionError("operador unario no permitido")

    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if not isinstance(left, (int, float)) or isinstance(left, bool):
            raise SafeExpressionError("operando izquierdo no numérico")
        if not isinstance(right, (int, float)) or isinstance(right, bool):
            raise SafeExpressionError("operando derecho no numérico")

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("division por cero")
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
        raise SafeExpressionError("operador binario no permitido")

    raise SafeExpressionError("expresión no permitida")


def calculate(expression: str) -> str:
    """
    Evalua una expresion matematica.

    Args:
        expression: Expresion aritmetica en texto.
                    Soporta: +, -, *, /, ** y parentesis.

    Returns:
        Resultado como string, o mensaje de error si la expresion es invalida.
    """
    if not isinstance(expression, str):
        return f"ERROR: 'expression' debe ser string, recibio {type(expression).__name__}"

    expression = expression.strip()
    if not expression:
        return "ERROR: expresion vacia"

    try:
        tree = ast.parse(expression, mode="eval")
        result: Any = _evaluate_node(tree.body)
        if isinstance(result, (int, float)) and not isinstance(result, bool):
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"
        return f"ERROR: resultado no es numerico: {type(result).__name__}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except SyntaxError as exc:
        return f"ERROR: sintaxis invalida: {exc.msg}"
    except SafeExpressionError as exc:
        return f"ERROR: {exc}"
    except ValueError as exc:
        return f"ERROR: {exc}"
