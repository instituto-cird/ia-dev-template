"""
agent/tools/calculator.py — Herramienta de cálculo matemático.

🚨 BUG 2: la IA generó esta versión con eval cuando le pedimos "calculadora
que acepte expresiones matemáticas en texto". eval ejecuta CUALQUIER código
Python, no solo aritmética. Si un usuario envía "calculate('__import__(\"os\").system(\"rm -rf /\")')"
el servidor lo ejecuta.

Comparar con la versión segura del template oficial que usa AST whitelist.
"""

import ast
import operator
from typing import Any

_ALLOWED_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.expr) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Operacion no permitida: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Evalua una expresion matematica usando un parser AST seguro.

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
        result = _eval_node(tree.body)
        if result == int(result):
            return str(int(result))
        return f"{result:.6g}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except Exception as e:
        return f"ERROR: {e}"