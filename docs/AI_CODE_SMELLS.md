# 👃 AI Code Smells (Guía de Auditoría)

En la era de los modelos frontera de 2026, el código se genera rápido, pero a menudo con "olores" específicos de IA. Antes de aprobar un PR (tuyo o de un agente), verifica esto.

> **Auditoría automática**: este checklist está implementado parcialmente en `tools/audit_code.py`.
> Corré `uv run python tools/audit_code.py` para que el script te marque los smells detectables por patrones. Los chequeos que requieren juicio humano (Parrot Comments, Complejidad Ciclomática) quedan a tu cargo.

## 1. El "Happy Path" Obsesivo
**Síntoma:** El código asume que las APIs nunca fallan, los archivos siempre existen y el usuario nunca se equivoca.
**Auditoría:**
- [ ] ¿Hay bloques `try/except` específicos (no `except Exception: pass`)?
- [ ] ¿Se validan las entradas con Pydantic antes de procesarlas?
- [ ] **Acción:** Pídele al agente: "Refactoriza para manejar errores de red y timeouts".

## 2. Alucinación de Librerías (Ghost Dependencies)
**Síntoma:** Importaciones que parecen lógicas (`from fastapi import AwesomeAuth`) pero no existen o cambiaron en la versión actual.
**Auditoría:**
- [ ] ¿Pasa el `uv sync` sin errores?
- [ ] ¿Has verificado en PyPI que el paquete tiene mantenimiento activo en 2026?

## 3. Comentarios "Loro" (Parrot Comments)
**Síntoma:** Comentarios que narran lo obvio.
- *Mal:* `x = x + 1 # Incrementa x`
- *Bien:* `x = x + 1 # Ajuste por error de indexación en la librería legacy`
**Auditoría:**
- [ ] Borrar comentarios redundantes generados por la IA.

## 4. Complejidad Ciclomática Escondida
**Síntoma:** La IA genera funciones de 100 líneas con 5 if/else anidados porque "funcionó a la primera".
**Auditoría:**
- [ ] Aplicar principio de Responsabilidad Única.
- [ ] **Acción:** Pídele al agente: "Extrae la lógica de validación a una función pura separada".

## 5. Security by Obscurity
**Síntoma:** Hardcoding de credenciales o lógica de seguridad débil sugerida por ejemplos antiguos.
**Auditoría:**
- [ ] Buscar `api_key = "..."` en el código.
- [ ] Verificar inyección SQL/XSS incluso si el código "se ve limpio".

## 6. Contexto Envenenado (Context Poisoning)
**Síntoma:** El historial de conversación acumula instrucciones contradictorias o ejemplos incorrectos que el modelo usa como "contexto verdadero". El modelo empieza a alucinarse a sí mismo: cree que ya ejecutó un paso que no ejecutó, "recuerda" una respuesta que nunca recibió, o sigue instrucciones de un mensaje anterior que fue sobrescrito.

**Cómo ocurre en la práctica:**
- Sesiones largas donde se corrigió el rumbo varias veces ("no, mejor hazlo así... espera, vuelve al original").
- Few-shot prompts con ejemplos erróneos que el modelo generaliza.
- Agentes con memoria acumulativa sin mecanismo de olvido o priorización.
- Contexto de 100k tokens donde el modelo "olvida" las instrucciones del sistema y sigue el texto más reciente.

**Auditoría:**
- [ ] Si usas un agente con historial, ¿tienes un límite de ventana o mecanismo de resumen?
- [ ] ¿El system prompt está al principio Y se repite al final en sesiones largas?
- [ ] **Acción:** Pídele al agente: "Resume en un párrafo qué instrucciones estás siguiendo actualmente". Si la respuesta contradice tu system prompt original, el contexto está envenenado.
- [ ] Reiniciar la sesión si el modelo responde de forma inconsistente con instrucciones que no cambiaron.

---

## Comandos de Detección Rápida

Corre estos comandos antes de cada PR. Si alguno falla, no mergees.

```bash
# 1. Estilo y errores comunes (Smells 3 y 4)
uv run ruff check .

# 2. Errores de tipos — detecta Ghost Dependencies antes de runtime (Smell 2)
uv run mypy app/ --ignore-missing-imports

# 3. Vulnerabilidades de seguridad conocidas (Smell 5)
uv run bandit -r app/ -ll -q

# 4. Credenciales hardcodeadas (Smell 5) — grep manual
grep -rn "api_key\s*=\s*['\"]" app/ agent/
grep -rn "password\s*=\s*['\"]" app/ agent/
grep -rn "secret\s*=\s*['\"]" app/ agent/

# 5. Logging de datos sensibles — obligatorio en contexto PCI (Smell 5 + 6)
grep -rn "logger.*amount\|print.*card\|log.*cvv" app/ agent/

# 6. Except genérico — síntoma del Smell 1
grep -rn "except Exception:\|except:\s*pass" app/ agent/
```

> **Regla de oro**: Si `ruff + mypy + bandit` pasan y los `grep` no encuentran nada,
> tu PR tiene el piso técnico mínimo para ser revisado.