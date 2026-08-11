# ============================================================================
# 🔴 HALLAZGO GLOBAL · CRÍTICO · SCOPE DRIFT DEL PRD
# ----------------------------------------------------------------------------
# El Escenario del Lab 2 es GET /api/v1/transacciones (consulta
# del historial). Este archivo declara el request para POST /transactions
# (creación), que NO existe en el PRD. Ejemplo típico de
# "motivated mislabeling" documentado por Anthropic: para completar la
# tarea el agente eligió el caso de uso más "prototípico" en su corpus
# (create endpoint) en vez del pedido (consulta con paginación cursor).
#
# → Ver bloque final del archivo con el PROMPT corregido para regenerar
#   el schema apuntando al endpoint correcto.
# ============================================================================

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints
# ✅ BUENO · usa Pydantic v2 (BaseModel + Annotated + StringConstraints)
# 💡 CORRECCIÓN MENOR · si vas a usar datetime (recomendado),
#    agregá `from datetime import datetime` al import.


class TransactionCreateRequest(BaseModel):
    """Schema de entrada para crear una transacción según el PRD.

    Este modelo solo valida el contrato de entrada. La lógica de negocio
    sigue en la capa de servicio y no debe mezclarse con estas reglas.
    """
    # ✅ BUENO · docstring separa explícitamente validación de reglas de
    #    negocio.
    # ⚠️ PROBLEMA · el nombre `TransactionCreateRequest` refuerza el scope
    #    drift · el PRD no tiene endpoint de creación.
    # 💡 CORRECCIÓN · si mantenés este modelo, renombralo a
    #    `TransactionRecord` o similar (representa la entidad, no el
    #    request de un endpoint que no existe).

    comercio_id: Annotated[
        str,
        StringConstraints(
            min_length=1,
            pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Identificador del comercio afiliado. Se exige un UUID canónico "
                "para asegurar que la transacción siempre se asocia a un comercio "
                "válido y determinista."
            )
        ),
    ]
    # ✅ BUENO · regex de UUID canónico correcta, no acepta cualquier string con guiones.
    # ✅ BUENO · `strip_whitespace=True` evita fallos por espacios accidentales.
    # ⚠️ PROBLEMA · `str` con regex es más frágil que usar `UUID` nativo.
    #    Pydantic v2 tiene soporte para UUID.
    # 💡 CORRECCIÓN MANUAL · reemplazar por:
    #      from uuid import UUID
    #      comercio_id: UUID = Field(description="...")
    #    Pydantic valida y devuelve un UUID real (no string), más limpio
    #    para el service layer.

    amount_cents: Annotated[
        int,
        Field(
            gt=0,
            description=(
                "Monto de la transacción en centavos. Se exige que sea mayor a cero "
                "porque un monto nulo o negativo no representa una transacción válida."
            ),
        ),
    ]
    # ✅ BUENO · `int` en centavos evita floats y problemas de redondeo.
    # ✅ BUENO · `gt=0` es una validación de dominio razonable a nivel schema.
    # ⚠️ PROBLEMA MENOR · sin límite superior. Un `amount_cents = 999999999999`
    #    pasa la validación. ¿El PRD tiene un tope? · si sí, agregá `le=<tope>`.
    # 💡 CORRECCIÓN · si el PRD define un monto máximo por transacción:
    #      Field(gt=0, le=100_000_000, description="...")  

    created_at: Annotated[
        str,
        StringConstraints(
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Fecha de creación de la transacción en formato ISO 8601 UTC. "
                "Se restringe a este formato para mantener un contrato determinista "
                "y evitar ambigüedades de zona horaria."
            )
        ),
    ]
    # ⚠️ PROBLEMA · REINVENTA LA RUEDA · Pydantic v2 valida `datetime`
    #    nativamente con soporte de timezone. El pattern manual pierde:
    #      · Fracciones de segundo válidas ("2026-08-06T12:00:00.123Z")
    #      · Otras zonas horarias con offset ("+02:00")
    #      · Casos borde reales de ISO 8601
    # 🔴 PROBLEMA · SEMÁNTICA · en un request de CREACIÓN, ¿por qué el
    #    cliente manda `created_at`? Debería generarlo el servidor
    #    (`datetime.now(UTC)` al persistir). Aceptar `created_at` del
    #    cliente permite falsificar timestamps.
    # 💡 CORRECCIÓN MANUAL · dos opciones:
    #    (a) Si es un request de creación real: ELIMINAR `created_at` del
    #        schema. El server lo asigna.
    #    (b) Si es un objeto de recepción (importar de otra fuente):
    #        from datetime import datetime
    #        created_at: datetime = Field(description="...")
    #        Pydantic valida ISO 8601 con timezone nativamente.

    status: Annotated[
        str,
        StringConstraints(
            pattern=r"^(pending|approved|rejected|refunded|cancelled)$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Estado de la operación. Se limita a los valores del PRD para "
                "garantizar consistencia del dominio y evitar estados inválidos."
            )
        ),
    ]
    # ⚠️ PROBLEMA · usa regex enum-like en vez de `Literal` de Python.
    #    `Literal` da:
    #      · Autocompletado en el IDE
    #      · Mejor documentación OpenAPI (dropdown en Swagger)
    #      · Errores más claros ("value is not a valid enumeration member")
    # 🔴 PROBLEMA SEMÁNTICO · en creación, aceptar `status=approved` desde
    #    el cliente permite crear transacciones ya aprobadas sin pasar
    #    por el flujo de autorización. Es una vulnerabilidad de dominio.
    # 💡 CORRECCIÓN MANUAL · dos capas:
    #    (a) Cambiar a Literal:
    #        from typing import Literal
    #        status: Literal["pending", "approved", "rejected", "refunded", "cancelled"]
    #    (b) Restringir a "pending" en creación (regla de negocio):
    #        En creación el status DEBE ser "pending". La transición a
    #        otros estados va en un endpoint separado con autorización.
    #        Esta restricción va en el SERVICE, no acá.

    authorization_code: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=32,
            pattern=r"^[A-Za-z0-9\-]+$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Código de autorización. Se restringe a caracteres alfanuméricos "
                "y guiones para mantener un formato estable y determinista."
            )
        ),
    ]
    # ✅ BUENO · límites de longitud claros (1-32) y charset restrictivo.
    # 🔴 PROBLEMA SEMÁNTICO · igual que `status`, el `authorization_code`
    #    lo genera el sistema de autorización · NO el cliente en un create.
    #    Si aparece acá, es porque este schema mezcla "request de creación"
    #    con "representación de una transacción existente".
    # 💡 CORRECCIÓN MANUAL · en un `TransactionCreateRequest` real:
    #    ELIMINAR `authorization_code`. Se agrega en el service cuando
    #    la transacción se autoriza (o en un update posterior).
    # ⚠️ PROBLEMA MENOR · `Optional`? Si el request puede llegar sin
    #    authorization_code todavía, debería ser opcional:
    #      authorization_code: Optional[str] = None

    pan_last4: Annotated[
        str,
        StringConstraints(
            min_length=4,
            max_length=4,
            pattern=r"^\d{4}$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Últimos 4 dígitos del PAN. Se exige exactamente 4 dígitos para "
                "cumplir la política de exposición mínima y evitar revelar datos sensibles."
            )
        ),
    ]
    # ✅ BUENO · pattern estricto de 4 dígitos exactos.
    # ✅ BUENO · comentario alineado con PCI-DSS (exposición mínima de PAN).
    # 🔴 PROBLEMA SEMÁNTICO · en creación de transacción, el cliente
    #    normalmente envía el PAN completo (o un token). El `pan_last4`
    #    es una vista derivada que se calcula en el service ANTES de
    #    persistir (`pan[-4:]`), no un campo del request.
    # 💡 CORRECCIÓN MANUAL · en el request de creación real:
    #      · Aceptar `pan_token: str` (token de tokenización · no el PAN)
    #        o `pan: str` con validación estricta (16 dígitos + Luhn check)
    #      · El service extrae los last4 antes de guardar
    #      · Nunca persistir el PAN completo (regulación PCI-DSS)


# ============================================================================
# RESUMEN DE HALLAZGOS · POR SEVERIDAD
# ============================================================================
#
# 🔴 CRÍTICOS (bloquean el uso en producción)
#   1. Scope drift · endpoint POST /transactions no existe en el PRD · el 
#       Lab 2  define GET /api/v1/transacciones
#   2. `created_at` desde el cliente permite falsificar timestamps
#   3. `status` desde el cliente permite crear transacciones ya aprobadas
#   4. `authorization_code` desde el cliente permite bypass de autorización
#   5. `pan_last4` en el request rompe el flujo típico de PAN completo →
#      tokenización → last4 derivado
#
# 🟠 MEDIOS (afectan mantenibilidad y calidad)
#   6. `created_at` como `str` con regex en vez de `datetime` nativo
#   7. `status` como regex en vez de `Literal[...]`
#   8. `comercio_id` como `str` en vez de `UUID` nativo
#
# 🟡 BAJOS (mejoras cosméticas)
#  9. Sin tope superior en `amount_cents`
#
# ============================================================================
# CORRECCIÓN POR PROMPT 
# ============================================================================
# #file:docs/prd/PRD.md
# #file:docs/architecture/diagrams/sequence_historial.md
#
# CONTEXTO:
# Stack: Python 3.12 · FastAPI · Pydantic v2 · pytest
# Clean Architecture · este archivo va en app/schemas/historial.py
# Endpoint: GET /api/v1/transacciones (consulta con filtros + paginación cursor)
#
# TAREA:
# Del PRD (Historia INVEST #1 y Reglas de negocio), generá el modelo
# Pydantic v2 para los query params de consulta del historial:
#   · desde: date · hasta: date · estado: Optional[Literal[...]]
#   · page_size: int (default 50) · cursor: Optional[str]
#
# REQUISITOS:
# · Validaciones estrictas: rango hasta-desde <= 90 días (@field_validator)
# · page_size entre 1 y 100 (Field(ge=1, le=100, default=50))
# · Usar Literal[...] para estado en vez de regex
# · Usar date/datetime nativos de Pydantic (no strings con regex)
# · Comentarios que expliquen POR QUÉ cada validación (trazabilidad al PRD)
# · Sin lógica de negocio (el enmascarado de PAN va en service, no en schema)
#
# RESTRICCIONES: solo código Python · sin datos reales · determinístico
# ============================================================================
