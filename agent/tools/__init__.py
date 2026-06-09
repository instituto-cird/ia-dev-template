"""
agent/tools — Herramientas disponibles para el agente ReAct.

Agrega aquí el import de tus herramientas nuevas para que sean accesibles
desde `agent.core` y desde los tests.
"""

from agent.tools.calculator import calculate
from agent.tools.merchant_lookup import lookup_merchant

__all__ = [
    "calculate",
    "lookup_merchant",
]
