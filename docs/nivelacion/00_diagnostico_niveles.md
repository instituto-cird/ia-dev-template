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

### Pregunta 4 — ¿Has creado un entorno virtual en Python?

¿Sabes qué hace `python3 -m venv .venv` y por qué existe?
¿Has instalado dependencias con `pip install -r requirements.txt`?

- **No** → Empieza en [Nivel 1](#nivel-1--python-y-web-básico)
- **Sí** → [Nivel 2](#nivel-2--herramientas-específicas-del-curso) — estás listo/a para el material del curso

---

## Resumen de niveles

| Nivel | Perfil | Tiempo estimado | Documento |
|-------|--------|-----------------|-----------|
| **0** | Sin experiencia en programación o terminal | 12–20 horas | `nivel_0_punto_de_partida.md` |
| **1** | Python básico, sin APIs ni entornos virtuales | 6–10 horas | `nivel_1_python_y_web_basico.md` |
| **2** | Python con algo de web, aprende herramientas del curso | 3–5 horas | `python_essentials.md` |

> ⚠️ **Sobre los tiempos**: son estimaciones reales, no tiempos de lectura.
> Incluyen el tiempo de instalar herramientas, encontrar errores, releer ejemplos
> y hacer las mini-prácticas. Si programas más de 3 años, divide por 2.
> Si es tu primer contacto con el tema, multiplica por 1.5.

---

## Criterio de salida: Lab 0

Sin importar desde qué nivel empieces, el objetivo es poder completar el **Lab 0**
que se entrega antes de la primera sesión:

```
Lab 0 — Verificación de entorno
□ Python 3.11+ instalado y accesible desde la terminal
□ Repositorio clonado desde GitHub con SSH
□ Entorno virtual creado y activado
□ pip install -r requirements.txt ejecutado sin errores
□ pytest corre sin errores (al menos 1 test pasa)
□ Archivo .env creado con MOCK_MODE=true
□ El servidor FastAPI arranca con uvicorn app.main:app
```

Si puedes marcar todos los puntos, estás listo/a para la Clase 1.
Si alguno falla, el documento de tu nivel tiene instrucciones para resolver los problemas más comunes.

---

## Nivel 0 — Punto de partida absoluto

**Para quién**: nunca has programado, o programaste hace mucho tiempo y partiste de cero.
También aplica si programas en otro lenguaje (Java, PHP, etc.) pero nunca usaste Python ni la terminal de forma habitual.

→ **Documento**: `nivel_0_punto_de_partida.md`
→ **Tiempo**: 12–20 horas (puede distribuirse en varias semanas antes del inicio)

Qué cubre:
- Qué es la terminal y cómo usarla (Mac, Windows, Linux)
- Instalar Python paso a paso con verificación
- Variables, funciones, listas, diccionarios en Python
- Qué es JSON y cómo se usa en programación
- Qué es HTTP y cómo funciona una API REST (sin código)
- Tu primer script Python funcional
- Instalar Git y clonar un repositorio

---

## Nivel 1 — Python y web básico

**Para quién**: conoces Python lo suficiente para no perderte, pero nunca has trabajado con APIs, entornos virtuales, o no te sientes cómodo/a con el flujo de un proyecto real.

→ **Documento**: `nivel_1_python_y_web_basico.md`
→ **Tiempo**: 6–10 horas

Qué cubre:
- Entornos virtuales: por qué existen y cómo usarlos
- pip y requirements.txt
- HTTP en profundidad: métodos, status codes, headers, body JSON
- Consumir una API con requests y httpx
- Variables de entorno (.env) y por qué no se suben a Git
- Leer un stack trace y encontrar el error
- Git: add, commit, push, pull, ramas básicas

---

## Nivel 2 — Herramientas específicas del curso

**Para quién**: tienes fluidez en Python y has consumido APIs, pero necesitas ponerte al día con las herramientas y patrones específicos del diplomado.

→ **Documento**: `python_essentials.md`
→ **Tiempo**: 3–5 horas

Qué cubre:
- Type hints y mypy
- Pydantic v2 (la v1 tiene sintaxis diferente — no mezcles)
- async/await con FastAPI
- pytest y cobertura de tests
- Manejo correcto de errores (sin `except: pass`)
