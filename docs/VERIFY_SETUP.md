# 🩺 Verificación de Setup

> **Cuándo usar este documento**: antes de la Clase 1, antes del Lab 4, y siempre que sospeches que algo no anda bien. Te ahorra horas de troubleshooting a ciegas.

---

## Comando único de verificación

```bash
bash scripts/verify_setup.sh
```

Este script corre **22 chequeos** distribuidos en 8 categorías:

1. **Herramientas del sistema** (Python 3.12, git, uv, Docker opcional)
2. **Estructura del proyecto** (pyproject, .env, carpetas)
3. **Dependencias del proyecto** (FastAPI, Pydantic, pytest)
4. **Backend** (importa y arranca, /health responde)
5. **Mock LLM** (importa, responde)
6. **Agente Track B** (MockLLMClient + tools)
7. **Harness de calidad** (ruff, mypy, bandit, pytest)
8. **Git** (status, remote)

Cada chequeo es independiente: si uno falla, los demás siguen corriendo.

---

## Cómo leer la salida

Tres tipos de resultado:

| Símbolo | Significado | Qué hacer |
|---------|-------------|-----------|
| `✓ OK` (verde) | El chequeo pasó | Nada — seguir |
| `✗ FAIL` (rojo) | El chequeo falló | Ver el "hint" al final del reporte |
| `⚠ NO` (amarillo) | Warning opcional — no bloquea | Opcional |

Al final del script ves un resumen:

```
══════════════════════════════════════════════════════════════════
  PASSED: 20/22   FAILED: 0   WARNINGS: 2
══════════════════════════════════════════════════════════════════

✅ Entorno listo para los Labs. Podés arrancar.
```

Si hay `FAILED > 0`, el script imprime **qué chequeos fallaron** y el hint exacto para cada uno.

---

## Qué hace cada categoría

### 1. Herramientas del sistema
Valida que Python 3.12+, git y uv están instalados y son accesibles desde tu shell.

### 2. Estructura del proyecto
Verifica que estás parado en la carpeta raíz del template y que los archivos críticos no faltan.

### 3. Dependencias
Confirma que `uv sync` corrió al menos una vez y que las libs core están importables.

### 4. Backend
Verifica que `app.main` importa sin errores y que el endpoint `/health` responde en proceso (sin levantar uvicorn).

### 5. Mock LLM
Verifica que `app.mock_llm` importa y que el endpoint `/v1/chat/completions` responde a un POST básico (también en proceso).

### 6. Agente Track B
Verifica que `MockLLMClient` está disponible (Lab 4 lo requiere) y que las tools ejemplo funcionan.

### 7. Harness
Corre el pipeline completo del CI localmente: ruff, mypy, bandit, pytest con cobertura.

### 8. Git
Confirma que estás en un repo git con remote configurado (necesario para entregar via GitHub Classroom).

---

## Cuándo ejecutarlo

**Obligatorio**:
- Antes de la Clase 1
- Después de hacer `git pull` con cambios importantes del template
- Antes de abrir cualquier PR de evaluación

**Recomendado**:
- Antes de la primera clase de cada módulo nuevo
- Después de cambiar tu versión de Python o uv
- Cuando algo no anda y no sabés por dónde empezar

**No es necesario**:
- Antes de cada commit
- Mientras estás programando en un Lab

---

## Cuando falla

Si algún chequeo falla, antes de pedir ayuda:

1. **Leé el "hint"** que el script imprime debajo de cada FAIL.
2. **Probá el comando del hint** y mirá la salida real.
3. **Revisá `docs/RUNBOOK_TROUBLESHOOTING.md`** que documenta los errores frecuentes.
4. **Si nada funciona**, publicá en el canal de soporte con:
   - Tu SO y versión
   - La salida completa de `bash scripts/verify_setup.sh`
   - El comando del hint que probaste y su salida

---

## Cómo extender el script

Si encontrás un chequeo que sería útil agregar, abrí un PR. Patrón:

```bash
# En scripts/verify_setup.sh, agregá una línea como:
check "Descripción corta del chequeo (max 50 chars)" \
      "comando-que-debe-pasar-silenciosamente" \
      "hint para el estudiante si falla"
```

`check` = falla si no pasa (mostrará FAIL).
`warn` = solo informa si no pasa (mostrará NO).

---

*Última actualización: junio 2026.*
