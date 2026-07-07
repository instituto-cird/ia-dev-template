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
**Track:** [ ] Track A — API End-to-End   [ ] Track B — Agente/Orquestación
**Estudiante:**
**Período:** Módulo ___ | Semanas ___

---

## Registro de decisiones asistidas por IA

### Entrada 001

| Campo | Detalle |
|-------|---------|
| **Fecha** | YYYY-MM-DD |
| **Herramienta** | Cursor / Claude Code / Copilot / ChatGPT / Otro |
| **Contexto** | ¿En qué parte del código estabas trabajando? (ej: "Escribiendo el endpoint POST /transactions") |
| **Prompt exacto (o resumen)** | Copia el prompt que usaste, o un resumen fiel si fue muy largo |
| **Sugerencia de la IA** | ¿Qué generó la IA? Incluye el fragmento de código relevante si es corto |
| **Decisión tomada** | ¿Aceptaste? ¿Modificaste? ¿Rechazaste? ¿Por qué? |
| **Impacto en el código** | Archivo(s) y función(es) afectadas |

**Razonamiento en tus palabras:**
> Escribe aquí por qué la sugerencia era correcta (o incorrecta) desde tu perspectiva
> como desarrollador. ¿Qué habrías hecho diferente sin la IA?

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

4. **¿Cómo cambió tu flujo de trabajo usar IA vs no usarla?** ¿Fuiste más rápido? ¿Cometiste errores distintos?

5. **Completa esta frase:** "Como Agent Manager, el mayor riesgo de usar IA sin supervisión en este proyecto habría sido..."

---

*Este documento es evaluado como parte del criterio "Dominio del proceso" (20% de la nota final).*
