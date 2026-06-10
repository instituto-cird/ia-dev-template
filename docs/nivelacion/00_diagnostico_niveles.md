# ¿Por qué ruta de nivelación debo empezar?

> Lee este documento primero. Te toma menos de 5 minutos y evita que pases
> horas en material que no necesitas, o que saltes material que sí necesitas.

---

## Responde estas preguntas en orden

### Pregunta 1 — ¿Puedes abrir una terminal y ejecutar un comando?

Por ejemplo: ¿sabes cómo abrir la Terminal en Mac, la PowerShell en Windows,
o una terminal en Linux? ¿Puedes escribir `python3 --version` y ver el resultado?

- **No** → Empieza en [Nivel 0](#nivel-0--punto-de-partida-absoluto)
- **Sí** → Continúa con la Pregunta 2

---

### Pregunta 2 — ¿Puedes escribir y ejecutar un script Python básico?

¿Puedes crear un archivo `.py`, escribir una función con parámetros y llamarla?
¿Sabes qué son las listas, los diccionarios y los bucles `for` en Python?

- **No** → Empieza en [Nivel 0](#nivel-0--punto-de-partida-absoluto)
- **Sí, pero con dificultad** → Empieza en [Nivel 1](#nivel-1--python-y-web-básico)
- **Sí, sin dificultad** → Continúa con la Pregunta 3

---

### Pregunta 3 — ¿Has consumido alguna vez una API REST?

¿Has hecho un `curl` o una llamada con `requests.get(url)` y recibido JSON como respuesta?
¿Sabes qué es un status code HTTP (200, 404, 500)?

- **No** → Empieza en [Nivel 1](#nivel-1--python-y-web-básico)
- **Sí** → Continúa con la Pregunta 4

---

### Pregunta 4 — ¿Has usado un gestor de dependencias en Python?

¿Sabés qué es un entorno virtual y por qué existe? Esto incluye haber usado
cualquiera de: `python -m venv`, `pip install`, `poetry`, `conda`, o `uv`.
El diplomado usa **`uv`** específicamente — si no lo conocés, no es un problema,
se enseña en el Nivel 2.

- **No** → Empieza en [Nivel 1](#nivel-1--python-y-web-básico)
- **Sí** → [Nivel 2](#nivel-2--herramientas-específicas-del-curso) — estás listo/a para el material del curso

---

## Resumen de niveles

| Nivel | Perfil | Documento |
|-------|--------|-----------|
| **0** | Sin experiencia en programación o terminal | `nivel_0_punto_de_partida.md` |
| **1** | Python básico, sin APIs ni entornos virtuales | `nivel_1_python_y_web_basico.md` |
| **2** | Python con algo de web, aprende herramientas del curso | `00_python_essentials.md` |

---

## Criterio de salida: Lab 0

Sin importar desde qué nivel empieces, el objetivo es poder completar el **Lab 0**
que se entrega antes de la primera sesión:

```
Lab 0 — Verificación de entorno
□ Python 3.12.x instalado y verificable con `python3 --version`
□ `uv` instalado y verificable con `uv --version`
□ Repositorio del Lab 0 aceptado y clonado desde GitHub Classroom
□ Archivo .env creado con `cp .env.example .env` 
□ `uv sync --all-groups` ejecutado sin errores
□ `bash scripts/verify_setup.sh` pasa los chequeos
□ Pull Request abierto con CI en verde
```

Si puedes marcar todos los puntos, estás listo/a.
Si alguno falla, el documento de tu nivel tiene instrucciones para resolver los problemas más comunes.

---

## Nivel 0 — Punto de partida absoluto

**Para quién**: nunca has programado, o programaste hace mucho tiempo y partiste de cero.
También aplica si programas en otro lenguaje (Java, PHP, etc.) pero nunca usaste Python ni la terminal de forma habitual.

→ **Documento**: `nivel_0_punto_de_partida.md`

Qué cubre:
- Qué es la terminal y cómo usarla (Mac, Windows, Linux)
- Instalar Python paso a paso con verificación
- Variables, funciones, listas, diccionarios en Python
- Qué es JSON y cómo se usa en programación
- Qué es HTTP y cómo funciona una API REST (sin código)
- Tu primer script Python funcional
- Instalar Git, crear cuenta de GitHub y clonar un repositorio
- Aceptar una tarea en GitHub Classroom (lo vas a hacer para el Lab 0)

---

## Nivel 1 — Python y web básico

**Para quién**: conoces Python lo suficiente para no perderte, pero nunca has trabajado con APIs, entornos virtuales, o no te sientes cómodo/a con el flujo de un proyecto real.

→ **Documento**: `nivel_1_python_y_web_basico.md`

Qué cubre:
- Entornos virtuales: por qué existen y cómo funcionan (concepto general)
- HTTP en profundidad: métodos, status codes, headers, body JSON
- Consumir una API con `httpx` (la librería del diplomado; también verás `requests` en tutoriales viejos)
- Variables de entorno (.env) y por qué no se suben a Git
- Leer un stack trace y encontrar el error
- Git: add, commit, push, pull, ramas básicas

> Aunque el Nivel 1 te enseña conceptos generales de Python, en el diplomado vamos a usar **`uv`** (no `pip`). El Nivel 2 te muestra los comandos específicos.

---

## Nivel 2 — Herramientas específicas del curso

**Para quién**: tienes fluidez en Python y has consumido APIs, pero necesitas ponerte al día con las herramientas y patrones específicos del diplomado.

→ **Documento**: `00_python_essentials.md`

Qué cubre:
- `uv` como gestor de proyectos: `uv sync`, `uv run --frozen`, `uv add`
- Type hints y mypy
- Pydantic v2 (la v1 tiene sintaxis diferente — no mezcles)
- async/await con FastAPI
- pytest y cobertura de tests
- Manejo correcto de errores (sin `except: pass`)
