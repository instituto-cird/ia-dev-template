"""
agent/tools/calculator.py — Herramienta de cálculo matemático segura mediante AST.
"""

import ast
import operator
from collections.abc import Callable
from typing import Any

# Operadores binarios permitidos
_SAFE_BIN_OPS: dict[type[ast.AST], Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

# Operadores unarios permitidos
_SAFE_UNARY_OPS: dict[type[ast.AST], Callable[[Any], Any]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_ast_node(node: ast.AST) -> int | float:
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)
    elif isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            return val
        raise ValueError(f"Tipo de constante no permitido: {type(val).__name__}")
    elif isinstance(node, ast.BinOp):
        bin_op_type: type[ast.AST] = type(node.op)
        if bin_op_type not in _SAFE_BIN_OPS:
            raise ValueError(f"Operador binario no permitido: {bin_op_type.__name__}")
        left_val = _eval_ast_node(node.left)
        right_val = _eval_ast_node(node.right)
        if bin_op_type is ast.Pow and isinstance(right_val, (int, float)) and abs(right_val) > 1000:
            raise ValueError("Exponente demasiado grande (máximo 1000)")
        res_bin: int | float = _SAFE_BIN_OPS[bin_op_type](left_val, right_val)
        return res_bin
    elif isinstance(node, ast.UnaryOp):
        unary_op_type: type[ast.AST] = type(node.op)
        if unary_op_type not in _SAFE_UNARY_OPS:
            raise ValueError(f"Operador unario no permitido: {unary_op_type.__name__}")
        operand_val = _eval_ast_node(node.operand)
        res_unary: int | float = _SAFE_UNARY_OPS[unary_op_type](operand_val)
        return res_unary
    else:
        raise ValueError(f"Expresión no permitida o insegura: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Evalua una expresion matematica de forma segura utilizando AST.

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
        parsed = ast.parse(expression, mode="eval")
        result: Any = _eval_ast_node(parsed)
        if isinstance(result, (int, float)):
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"
        return f"ERROR: resultado no es numerico: {type(result).__name__}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except (ValueError, SyntaxError, TypeError, MemoryError, OverflowError) as e:
        return f"ERROR: {e}"

