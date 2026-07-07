"""
agent/tools/calculator.py — Herramienta de cálculo matemático.

🚨 BUG 2: la IA generó esta versión con `eval` cuando le pedimos "calculadora
que acepte expresiones matemáticas en texto". `eval` ejecuta CUALQUIER código
Python, no solo aritmética. Si un usuario envía "calculate('__import__(\"os\").system(\"rm -rf /\")')"
el servidor lo ejecuta.

Comparar con la versión segura del template oficial que usa AST whitelist.
"""

from typing import Any


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
        # 🚨 `eval` es peligroso — acepta cualquier expresión Python,
        # no solo aritmética. Reemplazar por un parser AST seguro.
        result: Any = eval(expression)
        if isinstance(result, (int, float)):
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"
        return f"ERROR: resultado no es numerico: {type(result).__name__}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except Exception as e:
        return f"ERROR: {e}"
