# Uso de IA para contratos Pydantic

## Entrada 1 · Contratos Pydantic

### Objetivo
Generar contratos Pydantic para el endpoint de historial de transacciones.

### Herramienta y modelo
GitHub Copilot Chat.

### Contexto proporcionado
- docs/prd/PRD_v1.md

### Salida inicial
- app/schemas/models.py

### Problema detectado
Durante la auditoría se identificó que la IA infirió algunos elementos no definidos explícitamente en el PRD, como:
- date_from / date_to
- restricciones de longitud para status
- reglas adicionales de paginación

Estos elementos no estaban respaldados de forma explícita por los requisitos del documento y por lo tanto debieron revisarse antes de aceptarlos.

### Corrección humana
Se realizó una auditoría adicional para distinguir entre:
- requisitos explícitos del PRD
- supuestos generados por el modelo

Se aceptó el uso de:
- Decimal
- Request/Response separados
- ConfigDict(extra="forbid")

Esto último se justificó porque la consigna exige rechazar campos no definidos.

### Evidencia
- Archivo generado y auditado manualmente: app/schemas/models.py

### Pregunta abierta
Definir con mayor precisión los filtros de fecha y los valores válidos para estado en futuras iteraciones.

---

## Observación de control
La IA puede generar artefactos útiles y estructurados, pero requiere validación humana para separar requisitos explícitos de inferencias no documentadas. En este caso, la corrección final fue compatible con la intención del PRD y con la regla de rechazo de campos no definidos.

## Entrada 2 · Tests

Objetivo:
Generar una suite inicial de tests para el historial de transacciones.

Herramienta y modelo:
GitHub Copilot Chat.

Contexto proporcionado:
PRD_v1.md y app/schemas/models.py.

Salida inicial:
La IA generó tests que reproducían internamente la lógica de filtrado.

Problema detectado:
Los tests eran tautológicos porque calculaban el resultado esperado utilizando la misma lógica que posteriormente sería implementada en el sistema.

Corrección humana:
Se rechazó la propuesta inicial y se solicitó una nueva versión basada en comportamiento observable mediante TestClient y el endpoint GET /api/v1/transacciones.

Evidencia:
Borradores de tests auditados manualmente.

Pregunta abierta:
Definir el comportamiento exacto esperado cuando el rango solicitado supera los 90 días.

Evidencia adicional:

Se ejecutó:

uv run --frozen pytest -v

Resultado:

Los tres tests del historial fallaron con respuesta HTTP 404.

Interpretación:

La falla corresponde a la ausencia de implementación del endpoint GET /api/v1/transacciones, por lo que constituye una pantalla roja válida dentro del flujo TDD.

Problema detectado:
La IA mantuvo repetidamente constructores inválidos (init en lugar de __init__) incluso después de una solicitud explícita de corrección.

Corrección humana:
Se identificó el error mediante auditoría manual y se solicitó una corrección específica antes de aceptar el código.

## Entrada 3 · Refactor e implementación

Objetivo:
Implementar el endpoint GET /api/v1/transacciones utilizando una arquitectura con responsabilidades separadas.

Herramienta y modelo:
GitHub Copilot Chat.

Contexto proporcionado:
PRD_v1.md, models.py y test_historial.py.

Salida inicial:
La IA propuso una implementación separada en Router, Service y Repository.

Problema detectado:
La IA generó repetidamente constructores inválidos utilizando `init` en lugar de `__init__`, lo que impedía la correcta inicialización de las clases.

Corrección humana:
Se revisó manualmente el código y se corrigieron los constructores. Además se registró el router dentro de app/main.py para exponer correctamente el endpoint.

Evidencia:
pytest ejecutado exitosamente.

Resultado:
40 passed, 1 warning.

Justificación del patrón:
Se utilizó la separación Router → Service → Repository para aislar HTTP, lógica de negocio y acceso a datos, reduciendo el acoplamiento y facilitando las pruebas.