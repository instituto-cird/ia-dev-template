# Postmortem · Proyecto Final Alba Esquivel · 31/08/2026

## Qué funcionó

- El agente ReAct logró consultar las reglas definidas en el PRD mediante `buscar_regla_prd()` y utilizar la información recuperada como evidencia para responder.
- El uso del Mock LLM permitió probar el comportamiento del agente de forma reproducible, sin depender de una API externa.
- Trabajar de forma incremental y ejecutar tests, evals y lint durante el desarrollo ayudó a detectar errores antes de llegar a la entrega final.
- Utilizar IA como apoyo para generar una primera versión del código permitió avanzar más rápido, siempre realizando una revisión posterior de lo generado.

## Qué no funcionó

- Las respuestas generadas por IA no siempre estaban completamente alineadas con la información disponible. En algunos casos proponían campos, reglas o decisiones que no estaban definidas en el PRD.
- Algunos tests generados inicialmente daban una falsa sensación de seguridad porque utilizaban validaciones demasiado generales y no comprobaban exactamente el comportamiento esperado.
- Durante la integración con CI aparecieron errores de lint y formato que no afectaban el funcionamiento del código, pero impedían que el pipeline finalizara correctamente.
- Reconstruir posteriormente algunas decisiones tomadas con IA para documentarlas en `AI_USAGE.md` resultó más difícil que registrarlas en el momento.

## Qué haría distinto

- Registraría cada interacción importante con IA y la decisión tomada inmediatamente en `AI_USAGE.md`, en lugar de reconstruir el proceso al final.
- No aceptar importar librerias o herramientas innecesarias 
- Ejecutaría lint, tests y evals después de cada cambio relevante para detectar problemas más temprano.

## 3 lecciones aprendidas

1. **Sobre agentes:** aprendí que un agente no consiste solamente en llamar a un LLM. Necesita tools con contratos definidos, un ciclo de decisión controlado y barandas explícitas como el alcance mediante `SYSTEM_PROMPT` y el límite de ejecución mediante `MAX_STEPS`.

2. **Sobre RAG:** aprendí que recuperar información relevante y proporcionarla como contexto ayuda a fundamentar las respuestas, pero no garantiza que sean correctas. También es necesario evaluar si se recuperó la evidencia adecuada y si el modelo la interpretó correctamente.

3. **Sobre trabajo con IA:** aprendí a no tomar las respuestas de la IA como correctas automáticamente. Es necesario auditarlas contra la fuente de verdad, como el PRD. Cuando una regla, campo o comportamiento no está definido, es preferible marcarlo como supuesto o pregunta abierta y solicitar validación antes que permitir que la IA lo asuma o lo convierta en una decisión.