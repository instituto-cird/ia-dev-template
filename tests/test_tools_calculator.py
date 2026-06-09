"""
tests/test_tools_calculator.py — Suite de tests para `agent/tools/calculator.py`.

Patrón a seguir cuando escribas tus propias tools en Lab 4:
    - 1 test por caso feliz
    - N tests por casos borde (inputs inválidos)
    - 1 test por error esperado (no debe crashear, debe retornar string ERROR)
"""

from agent.tools.calculator import calculate

# ─── Casos felices ────────────────────────────────────────────────────────────


def test_calculate_simple_addition() -> None:
    assert calculate("2 + 3") == "5"


def test_calculate_complex_expression() -> None:
    # Mezcla de operadores con paréntesis
    assert calculate("(100 + 50) / 3") == "50"


def test_calculate_exponentiation() -> None:
    assert calculate("2 ** 10") == "1024"


def test_calculate_decimal_result() -> None:
    # Resultado con decimales
    result = calculate("10 / 3")
    assert result.startswith("3.33")


def test_calculate_negative_numbers() -> None:
    assert calculate("-5 + 10") == "5"


# ─── Casos borde / inputs inválidos ──────────────────────────────────────────


def test_calculate_empty_string_returns_error() -> None:
    result = calculate("")
    assert result.startswith("ERROR")


def test_calculate_non_string_returns_error() -> None:
    # El agente puede pasar un dict por error — no debe crashear
    result = calculate(42)  # type: ignore[arg-type]
    assert result.startswith("ERROR")


def test_calculate_division_by_zero() -> None:
    result = calculate("10 / 0")
    assert "division por cero" in result.lower() or result.startswith("ERROR")


def test_calculate_invalid_syntax() -> None:
    # Paréntesis sin cerrar — sintácticamente inválido en Python
    result = calculate("2 + (3")
    assert result.startswith("ERROR")


def test_calculate_dangling_operator() -> None:
    # Operador sin operando — sintácticamente inválido
    result = calculate("2 +")
    assert result.startswith("ERROR")


# ─── Seguridad: rechaza expresiones peligrosas ───────────────────────────────


def test_calculate_rejects_function_calls() -> None:
    # Una llamada a función debe ser rechazada (no es una expresión aritmética)
    result = calculate("__import__('os').system('ls')")
    assert result.startswith("ERROR")


def test_calculate_rejects_attribute_access() -> None:
    # Acceso a atributos debe ser rechazado
    result = calculate("foo.bar + 1")
    assert result.startswith("ERROR")


def test_calculate_rejects_variable_names() -> None:
    # Nombres de variable no deben evaluarse (sin contexto, son indefinidos)
    result = calculate("x + 1")
    assert result.startswith("ERROR")
