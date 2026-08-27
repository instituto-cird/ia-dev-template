# Postmortem · Proyecto Final Linda Riquelme · 27-ago

## Qué funcionó

- [Algo técnico concreto · ej: el retriever lexical alcanzó para el 100% del scope mínimo]
- [Algo de proceso · ej: hacer commits chicos me evitó merges complicados]
- [Algo con la IA · ej: el prompt de la guía produjo el agente completo en un solo shot]

## Qué no funcionó

- [Problema técnico · ej: el mock LLM al principio no interpretaba el system prompt bien]
- [Problema de tiempo · ej: subestimé el eval set adversarial]
- [Problema con la IA · ej: sin la aclaración de "determinístico = reproducible", Copilot hardcodeó reglas]

## Qué haría distinto

- [Cambio concreto 1]
- [Cambio concreto 2]

## 3 lecciones aprendidas

1. Sobre agentes: [ej: sin scope explícito el LLM alucina tools inexistentes]
2. Sobre RAG: [ej: grep lexical alcanza para dominios chicos · embeddings solo si escala]
3. Sobre trabajo con IA: [ej: escribir el AI_USAGE en tiempo real es mejor que reconstruirlo después]
