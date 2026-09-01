# AI_USAGE.md · Proyecto Final Alba Esquivel

## Entrada 1 · 2026-08-25

**Contexto:** generación del esqueleto inicial del agente RAG para responder consultas sobre reglas de negocio del PRD de Historial de Transacciones de LegacyPay.

**Herramienta IA:** Copilot Chat en Visual Studio Code.

**Prompt clave:** prompt canónico del Lab 4 utilizando `docs/prd/PRD.md` y `docs/agent/goal.md`, solicitando un agente RAG con patrón ReAct compuesto por `tools.py`, `loop.py` y `logger.py`.

**Decisión IA:** propuso el esqueleto del agente con la tool `buscar_regla_prd()`, `TOOLS_SCHEMA`, un loop ReAct donde el modelo decide entre buscar evidencia o responder, `SYSTEM_PROMPT`, `MAX_STEPS = 5` y un logger auditable.

**Decisión humana:** revisé los archivos generados y validé que el ciclo correspondiera realmente al patrón ReAct, es decir, que el LLM decidiera qué acción ejecutar en cada iteración y que el código no resolviera previamente el camino.

**Aprendizaje:** indicar explícitamente el patrón ReAct en el prompt es importante para obtener un agente donde el modelo toma decisiones dentro de límites, en lugar de un workflow lineal definido completamente por código.

---

## Entrada 2 · 2026-08-25

**Contexto:** generación de la tool de recuperación de información utilizada por el agente como mecanismo RAG simplificado.

**Herramienta IA:** Copilot Chat en Visual Studio Code.

**Prompt clave:** generar `buscar_regla_prd(termino: str) -> str` para buscar léxicamente información en `docs/prd/PRD.md`, devolver hasta 3 coincidencias con contexto y manejar término vacío, ausencia de coincidencias y PRD inexistente. También generar `TOOLS_SCHEMA` en formato OpenAI Chat Completions.

**Decisión IA:** implementó `buscar_regla_prd()` y definió el JSON Schema necesario para que el modelo conozca la tool y los argumentos disponibles.

**Decisión humana:** revisé que la herramienta se limitara a recuperar información del PRD, sin realizar modificaciones ni ejecutar acciones externas, y que manejara explícitamente los casos donde no existiera evidencia.

**Aprendizaje:** el schema de una tool define el contrato de entrada, pero las capacidades reales y sus límites deben seguir controlándose desde la aplicación. Para este agente, la tool solo necesita acceso de lectura.

---

## Entrada 3 · 2026-08-25

**Contexto:** implementación de trazabilidad y barandas para controlar la ejecución del agente.

**Herramienta IA:** Copilot Chat en Visual Studio Code.

**Prompt clave:** generar `logger.py` con registros JSONL después de cada ejecución de tool y un `loop.py` con dos barandas explícitas: alcance mediante `SYSTEM_PROMPT` y límite de ejecución mediante `MAX_STEPS = 5`.

**Decisión IA:** implementó el registro en `logs/agent_run.jsonl` con información del paso, tool, argumentos y resumen del resultado, además de las restricciones de scope y budget en el loop.

**Decisión humana:** validé mediante una consulta sobre el rango máximo del historial que el agente recuperara evidencia del PRD y mediante una consulta sobre la capital de Francia que rechazara una pregunta fuera de alcance.

**Aprendizaje:** las instrucciones del prompt no son la única protección del agente. Las barandas también deben estar representadas mediante controles explícitos, como el límite de pasos, y debe existir trazabilidad para revisar posteriormente las acciones ejecutadas.

---

## Entrada 4 · 2026-08-27

**Contexto:** creación de un Eval Set para comprobar el comportamiento del agente desarrollado anteriormente.

**Herramienta IA:** Copilot Chat en Visual Studio Code.

**Prompt clave:** generar `evals/eval_agent.py` con tres casos: `rango-90-dias`, `pan-solo-ultimos-4` y `fuera-de-alcance`, ejecutando `run_agent` contra el Mock LLM y mostrando PASS/FAIL para cada caso.

**Decisión IA:** generó un Golden Set con tres consultas y expectativas verificables sobre las respuestas del agente.

**Decisión humana:** ejecuté el Eval Set contra el Mock LLM y revisé los resultados de cada caso, en lugar de considerar una respuesta plausible como evidencia suficiente del correcto funcionamiento.

**Aprendizaje:** un Eval Set permite comparar el comportamiento del agente contra expectativas previamente definidas. Una respuesta que parece correcta no es suficiente; debe existir un criterio verificable para determinar PASS o FAIL.

---

## Entrada 5 · 2026-08-27

**Contexto:** revisión de las barandas del agente y preparación del código del Módulo 4 para continuar con el Proyecto Final.

**Herramienta IA:** Copilot Chat en Visual Studio Code.

**Prompt clave:** revisión del código generado para identificar explícitamente las barandas de alcance (`SYSTEM_PROMPT`) y presupuesto de ejecución (`MAX_STEPS = 5`).

**Decisión IA:** mantuvo las restricciones de alcance dentro del `SYSTEM_PROMPT` y el límite máximo de cinco iteraciones dentro del loop ReAct.

**Decisión humana:** agregué comentarios visibles en `app/agent/loop.py` identificando la baranda de SCOPE y la baranda de BUDGET, sin modificar su comportamiento.

**Aprendizaje:** una baranda debe poder identificarse y explicarse en el código. `SYSTEM_PROMPT` restringe el alcance de las respuestas, mientras que `MAX_STEPS` limita los recursos que el agente puede consumir durante una ejecución.