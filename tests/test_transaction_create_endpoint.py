# ============================================================================
# 🔴 HALLAZGO GLOBAL · SUITE INCOMPLETA + FALSOS VERDES
# ----------------------------------------------------------------------------
# Los 3 tests actuales dan verde pero su calidad de assert es baja. La regla
# de oro que enseñamos: "el verde es una hipótesis, no una prueba". Estos
# tests dejarían pasar implementaciones rotas (ver hallazgos por test).
#
# Aplicando los 6 riesgos:
#   1. Oráculo inventado ......... 🟡 Parcial (datos "prototípicos" sin fixture)
#   2. Test tautológico .......... ❌ No aplica
#   3. Mock excesivo ............. ❌ No aplica (TestClient real, sin mocks)
#   4. Happy path dominante ...... 🔴 SÍ (2 de 3 tests son 201, faltan 8+ casos)
#   5. API alucinada ............. ❌ No aplica (imports reales)
#   6. Falso verde ............... 🔴 SÍ (test 1 y 3 pasan aunque el server no haga nada)
#
# → Ver bloque final con correcciones.
# ============================================================================

from fastapi.testclient import TestClient
from app.main import app
# ✅ BUENO · usa la app real, no un mock. Los tests son de integración
#    a nivel de endpoint (bien para validar el contrato completo).
# ⚠️ PROBLEMA · si `app.main` no existe todavía (Paso 3 del TDD no hecho),
#    el import mismo falla. Verificá que el módulo exista antes de correr.


def test_create_transaction_returns_201_for_valid_payload() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 1500,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "approved",
        "authorization_code": "AUTH-001",
        "pan_last4": "4242",
    }
    # ✅ BUENO · patrón AAA con comentarios claros (# Arrange).
    # ✅ BUENO · nombre del test cumple la convención test_[qué]_[cuándo]_[resultado].
    # 🟡 RIESGO 1 (Oráculo inventado, leve) · los valores (1500, "AUTH-001", "4242")
    #    son "prototípicos" · no hay fixture centralizado ni comentario que
    #    los ancle al PRD. Si mañana cambia una regla, hay que buscar en
    #    cada test manualmente.
    # 💡 CORRECCIÓN · mover a un fixture en tests/conftest.py:
    #      @pytest.fixture
    #      def valid_transaction_payload() -> dict:
    #          return { ... }
    #    Y el test recibe `valid_transaction_payload` como parámetro.

    # Act
    response = client.post("/transactions", json=payload)
    # 🔴 SCOPE DRIFT · el endpoint /transactions no está en el PRD. 
    #   El PRD define GET /api/v1/transacciones.
    # 💡 CORRECCIÓN · corregir la URL:
    #      response = client.get("/api/v1/transacciones?desde=...&hasta=...")
    # ⚠️ PROBLEMA · falta el header Authorization Bearer. El endpoint del
    #    PRD requiere JWT. Sin header, en la implementación correcta el response 
    #   debería ser 401, no 201.

    # Assert
    assert response.status_code == 201
    # 🔴 RIESGO 6 (Falso verde, CRÍTICO) · este es el único assert.
    #    Si el endpoint devuelve 201 con body vacío, sin persistir nada,
    #    sin generar un ID, sin location header · el test pasa igual.
    #    El verde es cosmético · no valida el comportamiento real.
    # ❓ PREGUNTA P5 · ¿el verde es por lógica o por trivialidad? Trivial.
    # ❓ PREGUNTA P2 · ¿fallaría si la implementación estuviera mal? NO.
    # 💡 CORRECCIÓN MANUAL · agregar asserts sobre el comportamiento:
    #      body = response.json()
    #      assert "id" in body
    #      assert body["comercio_id"] == payload["comercio_id"]
    #      assert body["amount_cents"] == payload["amount_cents"]
    #      assert "Location" in response.headers  # convención REST


def test_create_transaction_returns_422_for_invalid_field() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 0,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "approved",
        "authorization_code": "AUTH-001",
        "pan_last4": "4242",
    }
    # ✅ BUENO · el payload es igual al happy path excepto por UN campo
    #    inválido (amount_cents=0). Esto aísla la variable a testear.
    # 💡 CORRECCIÓN · reutilizar el fixture del test anterior:
    #      def test_...(valid_transaction_payload):
    #          payload = {**valid_transaction_payload, "amount_cents": 0}

    # Act
    response = client.post("/transactions", json=payload)
    # 🔴 SCOPE DRIFT · mismo problema del test 1 (endpoint incorrecto).

    # Assert
    assert response.status_code == 422
    assert any(error["loc"][-1] == "amount_cents" for error in response.json()["detail"])
    # ✅ BUENO · TEST MÁS FUERTE de la suite. Verifica que:
    #    (a) el status es 422 (validation error)
    #    (b) el error específico está en el campo amount_cents
    # ✅ Este assert cazaría un falso verde: si Pydantic rechaza pero por
    #    OTRO campo, el test falla.
    # ❓ PREGUNTA P1 · ¿el assert compara con valor real? SÍ (loc del error).
    # ❓ PREGUNTA P2 · ¿fallaría si estuviera mal? SÍ (bien).
    # 💡 MEJORA MENOR · también verificar el "type" del error:
    #      assert any(
    #          e["loc"][-1] == "amount_cents" and e["type"] == "greater_than"
    #          for e in response.json()["detail"]
    #      )
    #    Así garantizás que el error es por `gt=0` y no por otra restricción.


def test_create_transaction_accepts_prd_boundary_values() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 1,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "cancelled",
        "authorization_code": "A" * 32,
        "pan_last4": "0000",
    }
    # ✅ BUENO · el intento es explorar valores de frontera:
    #    amount_cents=1 (mínimo válido por gt=0)
    #    authorization_code="A"*32 (longitud máxima)
    #    pan_last4="0000" (mínimo léxico válido)
    # 🟡 PROBLEMA · el docstring dice "boundary values" pero solo cubre
    #    fronteras VÁLIDAS. Faltan las fronteras INVÁLIDAS (una-más-allá
    #    del límite), que son las que suelen fallar en producción:
    #      · amount_cents = 0 (ya está en test 2)
    #      · authorization_code = "A" * 33 (uno más del máximo)
    #      · pan_last4 = "000" (uno menos)
    #      · pan_last4 = "00000" (uno más)
    # 💡 CORRECCIÓN · agregar tests separados para las fronteras inválidas
    #    (ver bloque de casos faltantes al final).

    # Act
    response = client.post("/transactions", json=payload)
    # 🔴 SCOPE DRIFT · mismo problema.

    # Assert
    assert response.status_code == 201
    # 🔴 RIESGO 6 (Falso verde) · mismo problema del test 1. Solo verifica
    #    status_code. La implementación puede estar rota y este test pasa.
    # ❓ PREGUNTA P3 · ¿cubre borde/error? Solo el borde VÁLIDO · faltan
    #    los bordes INVÁLIDOS que son los que exponen bugs.


# ============================================================================
# CASOS FALTANTES · lo que el PRD y las 5 preguntas exigen y NO está testeado
# ============================================================================
#
# 🔴 CRÍTICOS (autenticación y contrato)
#   [ ] test_returns_401_when_authorization_header_missing
#   [ ] test_returns_401_when_jwt_invalid_or_expired
#   [ ] test_returns_401_when_comercio_id_del_token_no_coincide_con_payload
#
# 🔴 CRÍTICOS (fronteras inválidas · Riesgo 4 · Happy Path Dominante)
#   [ ] test_returns_422_when_comercio_id_no_es_uuid
#   [ ] test_returns_422_when_status_no_esta_en_enum
#   [ ] test_returns_422_when_created_at_formato_invalido
#   [ ] test_returns_422_when_authorization_code_excede_32_chars
#   [ ] test_returns_422_when_pan_last4_tiene_letras
#   [ ] test_returns_422_when_pan_last4_tiene_menos_de_4_digitos
#
# 🟠 IMPORTANTES (schema strict + contrato)
#   [ ] test_returns_422_when_payload_tiene_campo_extra
#       (requiere model_config extra="forbid" en el schema · hoy pasaría 201)
#   [ ] test_returns_422_when_payload_esta_vacio
#   [ ] test_returns_422_when_falta_campo_requerido
#
# 🟠 IMPORTANTES (reglas de negocio del PRD)
#   [ ] test_returns_400_when_amount_cents_excede_tope (si el PRD tiene tope)
#   [ ] test_returns_400_when_intenta_crear_con_status_approved_directo
#       (regla de negocio: solo pending en creación)
#
# 🟡 DESEABLES (concurrencia y determinismo · Principio 2 CIRD)
#   [ ] test_dos_requests_simultaneos_con_mismo_payload_devuelven_ids_distintos
#   [ ] test_created_at_timezone_no_utc_es_rechazado_o_convertido
#
# ============================================================================
# CORRECCIÓN POR PROMPT 
# ============================================================================
#
# 📌 CAMINO A · REESCRIBIR TODA LA SUITE PARA EL ESCENARIO CORRECTO
# ---------------------------------------------------------------------------
# #file:docs/prd/PRD.md
# #file:docs/architecture/diagrams/sequence_historial.md
# #file:app/schemas/historial.py    # el schema regenerado del schema
#
# CONTEXTO:
# Stack: Python 3.12 · FastAPI · Pydantic v2 · pytest · TestClient
# El endpoint GET /api/v1/transacciones vive en app.main:app
# Autenticación: header Authorization: Bearer {JWT} · extrae comercio_id
# Aplicamos TDD asistido · estos tests van en ROJO hasta implementar el endpoint.
#
# TAREA:
# Reescribí la suite de tests con al menos 6 casos:
#   1. Happy Path · GET con desde/hasta válidos + JWT → 200 + shape correcto
#      (assert sobre "data", "pagination.next_cursor", "pagination.has_more")
#   2. Error 400 · rango mayor a 90 días → 400 + mensaje del PRD
#   3. Error 401 · sin header Authorization → 401
#   4. Error 401 · JWT malformado o expirado → 401
#   5. Error 422 · page_size fuera de rango (0 o 101) → 422 con campo específico
#   6. Caso borde · rango exacto de 90 días → 200 (frontera VÁLIDA)
#
# REQUISITOS:
# · Patrón AAA con comentarios (# Arrange · # Act · # Assert)
# · Fixture pytest para el payload/params base (evita duplicación)
# · Fixture pytest para el JWT válido (mock o token de prueba)
# · Asserts sobre COMPORTAMIENTO OBSERVABLE (status + shape) NUNCA solo status
# · Nombres: test_historial_[condición]_[resultado_esperado]
# · Comentar cuando un test cubre una regla específica del PRD 
#
# RESTRICCIONES: sin datos reales · sin red · determinístico · solo Python.
#
# ============================================================================
# CHECKLIST PRE-COMMIT · antes de aceptar cualquier test verde
# ============================================================================
#
# ☐ ¿Cada test tiene al menos 2 asserts?
# ☐ ¿Los asserts verifican COMPORTAMIENTO OBSERVABLE, no solo status code?
# ☐ ¿Hay al menos 1 test de error por cada regla del PRD?
# ☐ ¿Hay tests para todas las fronteras INVÁLIDAS (uno-más-allá del límite)?
# ☐ ¿Hay tests para autenticación (401)?
# ☐ ¿Hay tests para payload malformado (extra fields · faltantes · vacío)?
# ☐ ¿Los asserts identifican el campo específico en errores 422?
# ☐ ¿Un `grep -rn "assert True" tests/` NO devuelve nada?
# ☐ ¿Un `grep -rn "except" tests/` está justificado en cada aparición?
# ============================================================================
