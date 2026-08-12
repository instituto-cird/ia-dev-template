# AI_USAGE.md — Registro de Uso de IA

> **Instrucciones:** Documentá las instancias **significativas** en que usaste IA
> (Cursor, Claude Code, Copilot, ChatGPT, etc.) para escribir código o tomar
> decisiones de diseño. Es un entregable obligatorio para ambos tracks. La defensa
> puede incluir preguntas sobre cualquier entrada de este registro.

---

## 🎯 Heurística: ¿cuándo SÍ documento, cuándo NO?

**Documentás cuando hubo una decisión, no cuando hubo un autocomplete.**

### ✅ Documentá si...

- Reescribiste el prompt **3 o más veces** hasta llegar al output correcto
- El output **requirió debugging** (no funcionó al primer intento)
- La IA propuso **un diseño que aceptaste sin haberlo pensado antes**
- **Rechazaste** una sugerencia por seguridad, performance o correctitud
- La IA **inventó** algo (Ghost Dependency, API obsoleta, lógica fantasma) y lo detectaste
- Usaste la IA para **refactorizar** un bloque complejo, no solo una línea
- Hiciste un **cambio arquitectónico** con asistencia de IA

### ⛔ No hace falta documentar si...

- La IA completó un `import` o un nombre de variable obvio
- Reescribió un docstring trivial
- Generó **boilerplate** que ya sabías que ibas a escribir igual
- Renombró una variable de forma mecánica
- Te sugirió un `for` o un `if` que cualquier autocompletado clásico (no IA) también hubiera sugerido

### 🧭 Regla de oro

> *Si dentro de 3 meses no vas a saber por qué tu código quedó así → documentalo.
> Si es obvio → no.*

**Cantidad esperada:** un proyecto del M5 típicamente genera entre **5 y 15 entradas** significativas. Si pasaste de 25, probablemente estás sobre-documentando. Si tenés menos de 3, probablemente estás sub-documentando.

---

## Resumen del proyecto

**Nombre del proyecto:**
**Estudiante/s:**

---

## Registro de decisiones asistidas por IA

### Entrada 001

| Campo | Detalle |
|-------|---------|
| **Fecha** | 2026-0-12 |
| **Herramienta** | Antigravity + Gemini |
| **Contexto** | Corrección de error de tipos en calculator.py, remoción de import fantasma en core.py y mejora del manejo de excepciones en merchant_lookup.py.|
| **Prompt exacto (o resumen)** | Explicar error de tipos en calculator.py, corregir los AI Smells 
(GHOST_IMPORT y EXCEPT_PASS), y reemplazar except Exception por excepciones específicas.|
| **Sugerencia de la IA** | Usar isinstance para el narrowing de tipos, eliminar la dependencia falsa fastapi_magic_auth, agregar loggueo de errores en merchant_lookup.py y capturar la tupla de excepciones (ValueError, SyntaxError, TypeError, MemoryError, OverflowError). |
| **Decisión tomada** | Aceptada y ajustada. Se agregó SyntaxError de forma explícita para evitar que expresiones con sintaxis inválida hicieran fallar las pruebas unitarias. |
| **Impacto en el código** | calculator.py, core.py y merchant_lookup.py |

**Razonamiento en tus palabras:**
> La IA identificó correctamente los patrones de smells y propuso soluciones idiomáticas en Python. La decisión de añadir SyntaxError fue mía, basándome en el conocimiento de que las pruebas unitarias podrían exponer casos con sintaxis inválida que no fueron contemplados inicialmente. |

---

### Entrada 002

| Campo | Detalle |
|-------|---------|
| **Fecha** | YYYY-MM-DD |
| **Herramienta** | |
| **Contexto** | |
| **Prompt exacto (o resumen)** | |
| **Sugerencia de la IA** | |
| **Decisión tomada** | |
| **Impacto en el código** | |

**Razonamiento en tus palabras:**
>

---

<!-- Copia el bloque de "Entrada NNN" cuantas veces necesites -->

---

## Reflexión final

Responde al finalizar el proyecto (mínimo 100 palabras):

1. **¿En qué partes del proyecto la IA fue más útil?** ¿Por qué?

2. **¿En qué partes la IA generó código que tuviste que corregir?** Describe el error y cómo lo detectaste.

3. **¿Hubo alguna sugerencia de la IA que rechazaste completamente?** ¿Cuál fue tu razonamiento?

4. **¿Cómo cambió tu flujo de trabajo al usar IA vs no usarla?** ¿Fuiste más rápido? ¿Cometiste errores distintos?

5. **Completa esta frase:** "Como Agent Manager, el mayor riesgo de usar IA sin supervisión en este proyecto habría sido..."

