# AI_USAGE — Lab 2

## Entrada 1 — PRD

**Fecha:**
28/07/2026

**Objetivo:**
Generar un primer borrador del PRD para el historial de transacciones de LegacyPay.

**Herramienta y modelo:**
ChatGPT (GPT-5.5)

**Contexto proporcionado:**
Se proporcionó un prompt con el objetivo del PRD, hechos aprobados, restricciones, tareas y formato esperado. Se indicó no inventar reglas de negocio, SLA, volúmenes ni requisitos regulatorios, y marcar como PREGUNTA ABIERTA toda información no definida.

**Salida obtenida:**
La IA generó un PRD en formato Markdown con las secciones solicitadas: visión, alcance, usuarios, reglas de negocio, historias de usuario, restricciones no funcionales y preguntas abiertas.

**Problema detectado:**
La IA incorporó algunos supuestos y propuestas no respaldados por los hechos proporcionados, como funcionalidades adicionales, reglas de comportamiento por defecto y restricciones no definidas en el prompt.

**Cambio realizado por mí:**
Realicé una auditoría del PRD identificando los HECHOS, las PROPUESTAS IA, las PREGUNTAS ABIERTAS y las DECISIONES APROBADAS. Marcando con un comentario cada caso de la etiquetas identifiadas y dejé como preguntas abiertas los aspectos no definidos.

**Criterio o evidencia utilizada:**
Comparé cada sección del PRD con el prompt original y con los hechos aprobados para verificar al menos 1 ejemplo de cada etiqueta de auditoria solicitada para el Lab 2
**Pregunta todavía abierta:**
¿Cuál será el tamaño de página por defecto y el máximo permitido para la paginación?


## Entrada 2 — ERD

**Fecha:**  
28/07/2026

**Objetivo:**  
Generar un primer borrador del ERD lógico simplificado para la funcionalidad de historial de transacciones de LegacyPay, tomando como base el archivo `PRD.md`.

**Herramienta y modelo:**  
CHAP VISUAL ASK AUTO

**Contexto proporcionado:**  
Basado en el archivo PRD.md, generá un ERD lógico simplificado en Mermaid para la funcionalidad de historial de transacciones.

RESTRICCIONES
- No conviertas cada sustantivo en una tabla.
- No agregues campos, tablas ni relaciones no confirmadas sin marcarlas como propuesta.
- Incluí solo datos necesarios para filtros y visualización.
- No incluyas PAN completo, CVV ni datos de autenticación sensibles.
- No asumas que el ERD implementa por sí solo reglas de autorización, privacidad o concurrencia.

FORMATO
1. Bloque Mermaid.
2. Lista breve de supuestos.
3. Preguntas abiertas.

**Salida obtenida:**  
La IA generó un ERD en formato Mermaid con las entidades `MERCHANT` y `TRANSACTION`, una relación uno a muchos y los atributos necesarios para representar fecha, estado y monto. También incluyó una sección de supuestos y preguntas abiertas.

**Problema detectado:**  
La entidad `MERCHANT`, el campo `merchant_id` y la relación `MERCHANT → TRANSACTION` no estaban confirmados explícitamente en el PRD. El comercio autorizado estaba definido como actor de la funcionalidad, pero no necesariamente como una entidad del modelo de datos.

**Cambio realizado por mí:**  
Eliminé la entidad `MERCHANT`, su identificador y la relación con `TRANSACTION`. Mantuve únicamente la entidad `TRANSACTION` con los atributos mínimos necesarios para representar el historial.

**Criterio o evidencia utilizada:**  
¿Cada entidad está justificada por el PRD?
¿La IA convirtió un atributo o estado en tabla?
¿Las cardinalidades coinciden con las reglas conocidas?
¿Se agregaron entidades o campos no confirmados?
¿Aparecen datos sensibles innecesarios?
¿El diagrama renderiza correctamente?
¿Los supuestos y preguntas abiertas están visibles?


**Pregunta todavía abierta:**  
- ¿La vista debe soportar moneda explícita en el monto, o se asume una única moneda para este alcance?