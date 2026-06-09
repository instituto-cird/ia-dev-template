# DEMO_PLAN.md — Plan de Defensa del Proyecto Final

> **Instrucciones:** Completa este documento antes de tu Demo Day.
> El evaluador lo usa para seguir tu demostración en tiempo real.
> Tiempo total: 15 minutos de demo + 10 minutos de preguntas.
>
> **Regla:** Todo lo que aparezca aquí debe poder ejecutarse en vivo desde tu repo.
> Si hay un paso que "solo funciona en tu máquina", necesitas resolverlo antes.

---

## Datos del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | |
| **Track** | A — API End-to-End  /  B — Agente/Orquestación |
| **Repositorio** | https://github.com/[org]/[tu-repo] |
| **Estudiante** | |
| **Demo Day (fecha)** | |

---

## Estado del CI antes de la defensa

> Pega aquí una captura o el link al último run de CI en verde:

```
GitHub Actions URL: https://github.com/[org]/[tu-repo]/actions/runs/[id]
Estado: ✅ All checks passed
```

---

## Guión de la demo (15 minutos)

### Bloque 1 — Contexto del problema (2 min)

**Lo que dirás:**
> Describe el problema que resuelve tu proyecto en 3-4 oraciones. No asumas que el evaluador conoce LegacyPay en detalle.

**Slides / materiales de apoyo:**
- [ ] Ninguno (demo en vivo desde el terminal)
- [ ] README abierto en el navegador
- [ ] Otro: ___

---

### Bloque 2 — Arranque y CI (2 min)

**Comandos a ejecutar en orden:**

```bash
# 1. Mostrar que el repo está limpio
git status
git log --oneline -5

# 2. Instalar dependencias
uv sync

# 3. Correr el harness completo
uv run --frozen ruff check .
uv run --frozen mypy app/ --ignore-missing-imports
uv run --frozen bandit -r app/ -ll -q
uv run --frozen pytest -q --cov=app --cov-report=term-missing

# 4. Mostrar cobertura: debe ser >= 60%
```

**¿Qué mostrarás que funciona?**
- CI verde con todos los checks
- Cobertura mínima de 60%

---

### Bloque 3 — Demo de la funcionalidad principal (6 min)

> Detalla los pasos exactos de la demo. Sé específico — el evaluador debe poder seguirte.

**Paso 1:**
```bash
# Comando o acción
```
**Qué se ve:** ___
**Qué explicarás:** ___

**Paso 2:**
```bash
# Comando o acción
```
**Qué se ve:** ___
**Qué explicarás:** ___

**Paso 3:**
```bash
# Comando o acción
```
**Qué se ve:** ___
**Qué explicarás:** ___

<!-- Track B: incluye al menos un ciclo ReAct completo (Thought → Action → Observation → FINISH) -->
<!-- Track A: incluye al menos un flujo POST → validación Pydantic → respuesta tipada -->

---

### Bloque 4 — Decisión de diseño asistida por IA (3 min)

**La decisión que mostrarás:**
> Describe una decisión específica de tu AI_USAGE.md que quieras destacar.

**El código relevante:**
```python
# Pega aquí el fragmento de código en cuestión
```

**Lo que dirás:**
> "Usé [herramienta] para [propósito]. La sugerencia original era [X].
> La modifiqué porque [razón técnica]. El resultado final es [Y] y lo
> puedo defender porque [razonamiento]."

---

### Bloque 5 — Edge case o escenario de error (2 min)

**El edge case que mostrarás:**
> Ej: "Una transacción que supera el límite del comerciante" /
> "Un merchant_id inválido pasado al agente" / "El LLM responde con JSON malformado"

**Comando o acción:**
```bash
# Cómo reproducirlo
```

**Cómo lo maneja tu código:**
> Explica aquí el comportamiento esperado (no solo "no crashea").

---

## Preguntas frecuentes — Prepárate para responder

Las siguientes preguntas son comunes en la defensa. Escribe tu respuesta preparada:

**1. "¿Por qué elegiste FastAPI sobre Flask/Django?"**
> Tu respuesta:

**2. "¿Qué hace exactamente este test? ¿Por qué lo escribiste así?"**
> Elige un test de tu suite y prepara la explicación:

**3. "Si tuvieras una semana más, ¿qué mejorarías?"**
> Tu respuesta (sé honesto, no digas "nada"):

**4. [Track A] "¿Cómo escalaría este endpoint si recibiera 1000 requests/segundo?"**
> Tu respuesta:

**4. [Track B] "¿Cómo garantizas que el agente no entre en un loop infinito?"**
> Tu respuesta: (hint: MAX_STEPS y ACTIONS_REQUIRING_APPROVAL)

**5. "¿Cuál es el AI Code Smell más común que encontraste en el código que generó la IA?"**
> Tu respuesta:

---

## Checklist de la noche anterior

- [ ] `git pull` del repo — asegúrate de tener la versión correcta
- [ ] CI verde en `main`
- [ ] `uv sync` funciona desde cero en una carpeta limpia
- [ ] Los comandos del Bloque 2 y 3 corren sin errores
- [ ] DEMO_PLAN.md está commitado y pusheado
- [ ] AI_USAGE.md está completo con la reflexión final
- [ ] README.md tiene las instrucciones de setup correctas
- [ ] Tienes la URL del repositorio lista para compartir pantalla

---

*La defensa se evalúa según: Funcionalidad (40%) · Calidad técnica (30%) · Dominio del proceso (20%) · Comunicación (10%).*
