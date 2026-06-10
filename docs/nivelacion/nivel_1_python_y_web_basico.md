# Nivel 1 — Python y Web Básico

> **Para quién**: conocés Python lo suficiente para no perderte con funciones y listas,
> pero nunca trabajaste con APIs, entornos virtuales, variables de entorno,
> o no te sentís cómodo/a leyendo un error de Python.
>
> **Prerequisito**: completá el Nivel 0, o verificá que podés hacer el mini proyecto
> del final de ese documento sin dificultad.

---

## Parte 1 — Entornos virtuales: por qué existen

### El problema sin entornos virtuales

Imaginá que instalás la librería `httpx` versión 0.25 para un proyecto. Después instalás otro proyecto que necesita `httpx` versión 0.27. Python solo puede tener una versión instalada globalmente → uno de los proyectos se rompe.

Los **entornos virtuales** resuelven esto creando una instalación de Python aislada por proyecto. Cada proyecto tiene sus propias librerías, sin interferir con los demás.

### El enfoque tradicional (`venv` + `pip`) — referencial

Históricamente esto se hace con dos pasos:

```bash
python3 -m venv .venv             # crea el entorno virtual
source .venv/bin/activate          # lo activa (Linux/macOS)
pip install -r requirements.txt    # instala las librerías listadas
```

Este patrón fue estándar durante más de 10 años. **Lo mencionamos para que lo reconozcas en tutoriales y documentación que vas a leer**, pero no es el que vas a usar en el diplomado.

### El enfoque del diplomado: `uv`

El diplomado usa **`uv`** (escrito en Rust por Astral) que reemplaza `venv` + `pip` + `pip-tools` + `pyenv` en un solo binario. La razón es simple: cuando le pedís a una IA que sugiera una librería nueva, `uv` la instala en milisegundos. Con `pip` puede tardar 30 segundos cada vez — y en 90 minutos de práctica, esa diferencia se siente.

Los comandos clave los vas a aprender en el **Nivel 2** (`00_python_essentials.md`). Por ahora, basta con saber:

- `uv sync --all-groups` reemplaza el flujo de `venv` + `pip install -r requirements.txt`
- `uv run --frozen <comando>` reemplaza `source .venv/bin/activate` + `<comando>`
- El proyecto del diplomado **no tiene** `requirements.txt` — todo vive en `pyproject.toml` + `uv.lock`

---

## Parte 2 — Variables de entorno y archivos .env

### Qué son las variables de entorno

Una variable de entorno es una configuración que existe fuera del código. Se usa para:
- Guardar API keys, contraseñas, y datos sensibles (nunca hardcodeados en el código)
- Cambiar el comportamiento del programa entre desarrollo y producción
- Configurar rutas, puertos, y URLs sin modificar el código

```python
import os

# Leer una variable de entorno
api_key = os.environ.get("MI_API_KEY")
puerto = os.environ.get("PORT", "8000")    # "8000" es el valor por defecto

print(api_key)     # None si no está definida
print(puerto)      # "8000" si PORT no está definida
```

### Archivos .env — la forma práctica de manejarlas

En lugar de definir variables de entorno en el sistema, se usan archivos `.env`:

```bash
# Archivo: .env (en la raíz del proyecto)
MI_API_KEY=sk-abc123def456
PORT=8000
MOCK_MODE=true
DATABASE_URL=sqlite:///./datos.db
```

Y en Python se leen automáticamente con `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()    # Lee el archivo .env y carga las variables

api_key = os.environ.get("MI_API_KEY")
print(api_key)    # sk-abc123def456
```

### La regla más importante: .env nunca va a Git

El archivo `.env` contiene secretos. Si lo subes a GitHub, cualquier persona puede verlos.

```bash
# Verificar que .gitignore incluye .env
cat .gitignore | grep .env

# Si no está, agrégalo:
echo ".env" >> .gitignore
```

El proyecto del diplomado incluye:
- `.env.example` — un archivo de ejemplo sin valores reales, que SÍ va a Git
- `.gitignore` — ya configurado para excluir `.env`

```bash
# Al clonar el proyecto, copia el ejemplo y completa tus valores:
cp .env.example .env
# Luego edita .env con tus datos reales
```

---

## Parte 3 — HTTP en profundidad

### Cómo funciona una solicitud HTTP por dentro

Cuando tu código hace `requests.get("https://api.ejemplo.com/usuarios")`, esto pasa:

1. Tu computadora resuelve `api.ejemplo.com` a una dirección IP
2. Se establece una conexión TCP con el servidor
3. Tu programa envía una solicitud HTTP:

```
GET /usuarios HTTP/1.1
Host: api.ejemplo.com
Accept: application/json
Authorization: Bearer tu-token
```

4. El servidor procesa la solicitud y responde:

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 245

[{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Bob"}]
```

5. `requests` te entrega el objeto `Response` con todo esto.

### Trabajar con la respuesta

```python
import requests

respuesta = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# Status code
print(respuesta.status_code)      # 200

# Headers de la respuesta
print(respuesta.headers["Content-Type"])    # application/json; charset=utf-8

# Cuerpo como texto
print(respuesta.text)             # string JSON

# Cuerpo como diccionario Python (solo funciona si es JSON válido)
datos = respuesta.json()
print(datos["title"])

# Lanzar error automáticamente si el status es 4xx o 5xx
respuesta.raise_for_status()      # No hace nada si status es 200
```

### Enviar datos: POST con JSON

```python
import requests

# POST con un body JSON
nuevo_post = {
    "title": "Mi primer post",
    "body": "Este es el contenido",
    "userId": 1
}

respuesta = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=nuevo_post    # `json=` convierte el dict a JSON y agrega el header Content-Type
)

print(respuesta.status_code)    # 201 Created
print(respuesta.json())         # El recurso creado (con su id asignado)
```

### Headers de autenticación

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("MI_API_KEY")

# API Key en header
respuesta = requests.get(
    "https://api.ejemplo.com/datos",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
)
```

### Usar httpx — la alternativa async

El diplomado usa `httpx` en lugar de `requests` porque soporta código asíncrono.
La API es casi idéntica:

```python
import httpx

# Síncrono (igual que requests)
with httpx.Client() as client:
    respuesta = client.get("https://jsonplaceholder.typicode.com/users")
    datos = respuesta.json()
    print(datos[0]["name"])

# Asíncrono (lo usarás en los labs de FastAPI)
import asyncio

async def obtener_usuarios():
    async with httpx.AsyncClient() as client:
        respuesta = await client.get("https://jsonplaceholder.typicode.com/users")
        return respuesta.json()

# Ejecutar la función async:
usuarios = asyncio.run(obtener_usuarios())
print(usuarios[0]["name"])
```

---

## Parte 4 — Leer errores de Python (Stack Traces)

Uno de los skills más importantes para un desarrollador es leer errores. Python tiene errores muy descriptivos si sabes dónde mirar.

### Anatomía de un error

```
Traceback (most recent call last):
  File "app/main.py", line 23, in procesar_pedido
    total = calcular_total(items)
  File "app/calculadora.py", line 8, in calcular_total
    return sum(item["precio"] for item in items)
  File "app/calculadora.py", line 8, in <genexpr>
    return sum(item["precio"] for item in items)
KeyError: 'precio'
```

Cómo leerlo:
1. **Lee el final primero**: `KeyError: 'precio'` — este es el error real. El diccionario no tiene la clave `'precio'`.
2. **Lee el traceback de abajo hacia arriba**: la última línea mencionada es donde ocurrió el error (`calculadora.py`, línea 8).
3. **Sigue la cadena hacia arriba**: esa función fue llamada desde `main.py`, línea 23.

### Errores comunes y qué significan

```python
# NameError — usaste una variable que no existe
print(resultado)    # NameError: name 'resultado' is not defined
# Fix: define 'resultado' antes de usarla

# KeyError — clave que no existe en el diccionario
datos = {"nombre": "Ana"}
print(datos["edad"])    # KeyError: 'edad'
# Fix: verifica con 'if "edad" in datos' o usa .get("edad")

# TypeError — tipo de dato incorrecto
"hola" + 5    # TypeError: can only concatenate str (not "int") to str
# Fix: convierte al tipo correcto: "hola" + str(5)

# AttributeError — método o atributo que no existe
texto = "hola"
texto.push("!")    # AttributeError: 'str' object has no attribute 'push'
# Fix: el método correcto para str es 'texto + "!"' o f"{texto}!"

# IndexError — índice fuera del rango de la lista
lista = [1, 2, 3]
lista[5]    # IndexError: list index out of range
# Fix: verifica que el índice sea menor que len(lista)

# ImportError — módulo que no está instalado o el nombre es incorrecto
import pandas    # ModuleNotFoundError: No module named 'pandas'
# Fix: pip install pandas (dentro del entorno virtual activado)

# ValueError — valor correcto en tipo, pero inválido para la operación
int("hola")    # ValueError: invalid literal for int() with base 10: 'hola'
# Fix: verifica que el string sea un número antes de convertir
```

### Estrategia para resolver errores

1. **Lee el error completo** — no te detengas en la primera línea roja
2. **Busca el nombre del archivo y número de línea** donde ocurrió
3. **Copia el mensaje de error** (no la traza completa) y búscalo en internet o pregunta a un LLM
4. **Agrega un `print()`** antes de la línea que falla para ver qué contienen las variables
5. **Prueba una cosa a la vez** — no hagas múltiples cambios simultáneos

---

## Parte 5 — Git: ramas y trabajo colaborativo

El Nivel 0 cubrió los comandos básicos. Aquí añadimos el flujo con ramas, que es lo que usarás en el diplomado.

### Por qué usar ramas

Una rama es una copia del código donde puedes hacer cambios sin afectar la versión principal. Cuando terminas, integras (merge) tus cambios.

```
main:      A ─── B ─── C ─────────────── F
                  \                     /
mi-feature:        D ─── E ─────────────
```

### Flujo de trabajo del diplomado

```bash
# Ver en qué rama estás
git branch

# Crear una rama nueva y cambiarte a ella
git checkout -b mi-feature

# Hacer cambios, agregar y commitear normalmente
git add .
git commit -m "Implementa la función de validación"

# Enviar la rama a GitHub (la primera vez)
git push -u origin mi-feature

# En GitHub: crear un Pull Request de 'mi-feature' hacia 'main'
# (esto lo hace el instructor o el equipo)

# Actualizar tu copia local con los cambios de main
git checkout main
git pull

# Volver a tu rama y traer los cambios de main
git checkout mi-feature
git merge main
```

### Ver el historial

```bash
git log --oneline    # Lista compacta de commits
git log --oneline --graph --all    # Vista gráfica de ramas
git diff             # Ver qué cambió desde el último commit
git status           # Ver qué archivos están modificados o sin guardar
```

---

## Práctica final — Verificá que podés hacer esto

Antes de pasar al Nivel 2, completá este mini check. Si te traba alguno, el Nivel 2 te enseña los comandos exactos:

```bash
# 1. Crear una carpeta de práctica — no es necesario clonar el template todavía
mkdir ~/practica-nivel1
cd ~/practica-nivel1

# 2. Crear un entorno virtual y activarlo
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux  |  .venv\Scripts\activate en Windows

# 3. Instalar httpx y consumir una API
pip install httpx
python3 -c "import httpx; r = httpx.get('https://jsonplaceholder.typicode.com/users/1'); print(r.json()['name'])"
# Debería imprimir: Leanne Graham

# 4. Desactivar el entorno
deactivate
```

Si ese flujo te corrió sin errores, **el concepto de entornos virtuales te quedó claro**. Ahora pasá al Nivel 2 — ahí vas a aprender a hacer lo mismo con `uv`, que es lo que el template del diplomado espera.

> **El "setup real" del Lab 0** (clonar desde GitHub Classroom + `uv sync` + `verify_setup.sh` + PR) está documentado en Moodle (Módulo 0). No lo hagas todavía — primero terminá el Nivel 2.

---

*Continuá con* → `00_python_essentials.md` (Nivel 2)
