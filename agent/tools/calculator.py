"""
agent/tools/calculator.py — Herramienta de cálculo matemático.

Una herramienta bien escrita tiene:
    1. Docstring con descripcion, args y returns (el LLM lo usa para saber cómo llamarla).
    2. Validación de entrada (no confíes en que el LLM pase los tipos correctos).
    3. Manejo de errores explícito (nunca `except: pass`).
    4. Tests propios en tests/test_tools.py.
"""

import ast
import operator
from typing import Any

# Operadores permitidos — whitelist explícita, no eval abierto
_SAFE_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.expr) -> float:
    """Evalua un nodo AST con operadores aritmeticos seguros."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Tipo no permitido: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Operador no permitido: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _SAFE_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Operador unario no permitido: {op_type.__name__}")
        return _SAFE_OPS[op_type](_safe_eval(node.operand))
    raise ValueError(f"Expresion no soportada: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Evalua una expresion matematica de forma segura (sin usar eval).

    Args:
        expression: Expresion aritmetica en texto.
                    Soporta: +, -, *, /, ** y parentesis.
                    Ejemplos: "42 * 7", "(100 + 50) / 3", "2 ** 10"

    Returns:
        Resultado como string, o mensaje de error si la expresion es invalida.

    Uso desde el agente:
        action: "calculate"
        action_input: {"expression": "1500 * 1.08"}
    """
    if not isinstance(expression, str):
        return f"ERROR: 'expression' debe ser string, recibio {type(expression).__name__}"

    expression = expression.strip()
    if not expression:
        return "ERROR: expresion vacia"

    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        # Formateo limpio: entero si no hay decimales significativos
        if result == int(result):
            return str(int(result))
        return f"{result:.6g}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except ValueError as e:
        return f"ERROR: {e}"
    except SyntaxError:
        return f"ERROR: expresion invalida: '{expression}'"