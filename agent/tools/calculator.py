import ast
import operator as op
from typing import Any

_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError("operador no permitido")
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        return float(_ALLOWED_BINOPS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            raise ValueError("operador unario no permitido")
        return float(_ALLOWED_UNARYOPS[type(node.op)](_eval_ast(node.operand)))
    if isinstance(node, ast.Constant):  # Python 3.8+
        val = node.value
        if isinstance(val, (int, float)):
            return float(val)
        raise ValueError("constante no numerica")
    if isinstance(node, ast.Num):  # older AST node
        val = node.n
        if isinstance(val, (int, float)):
            return float(val)
        raise ValueError("constante no numerica")
    raise ValueError(f"nodo no permitido: {type(node).__name__}")


def calculate(expression: str) -> str:
    if not isinstance(expression, str):
        return (
            f"ERROR: 'expression' debe ser string, recibio {type(expression).__name__}"
        )

    expression = expression.strip()
    if not expression:
        return "ERROR: expresion vacia"

    try:
        parsed = ast.parse(expression, mode="eval")

        # Rechazar cualquier nodo peligrosamente dinámico (calls, names, attributes, subscripts, etc.)
        for n in ast.walk(parsed):
            if isinstance(
                n, (ast.Call, ast.Name, ast.Attribute, ast.Subscript, ast.Lambda)
            ):
                raise ValueError("expresion contiene elementos no permitidos")

        result_any: Any = _eval_ast(parsed)

        if isinstance(result_any, (int, float)):
            result = float(result_any)
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"
        return f"ERROR: resultado no es numerico: {type(result_any).__name__}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except SyntaxError as e:
        return f"ERROR: {e}"
    except ValueError as e:
        return f"ERROR: {e}"
