# Nivel 1 — Python y Web Básico

> **Para quién**: conoces Python lo suficiente para no perderte con funciones y listas,
> pero nunca has trabajado con APIs, entornos virtuales, variables de entorno,
> o no te sientes cómodo/a leyendo un error de Python.
>
> **Tiempo estimado**: 6–10 horas.
>
> **Prerequisito**: completa el Nivel 0, o verifica que puedes hacer el mini proyecto
> del final de ese documento sin dificultad.

---

## Parte 1 — Entornos virtuales: por qué existen

### El problema sin entornos virtuales

Imagina que instalas la librería `requests` versión 2.28 para un proyecto. Luego instalas otro proyecto que necesita `requests` versión 2.25. Python solo puede tener una versión instalada globalmente → uno de los proyectos se rompe.

Los **entornos virtuales** resuelven esto creando una instalación de Python aislada por proyecto. Cada proyecto tiene sus propias librerías, sin interferir con los demás.

### Crear y activar un entorno virtual

```bash
# 1. Entra a la carpeta de tu proyecto
cd mi-proyecto

# 2. Crea el entorno virtual (se llama .venv por convención)
python3 -m venv .venv

# 3. Activa el entorno virtual

# Mac/Linux:
source .venv/bin/activate

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# Sabrás que está activado porque el prompt cambia:
# (de)  user@machine:~/mi-proyecto$
# (a)   (.venv) user@machine:~/mi-proyecto$
```

### Usar el entorno activado

```bash
# Instalar una librería DENTRO del entorno (no globalmente)
pip install requests

# Verificar que se instaló en el entorno, no en el sistema
which python3     # Mac/Linux → debería apuntar a .venv/bin/python3
where python      # Windows

# Desactivar el entorno cuando terminas de trabajar
deactivate
```

> ⚠️ **Regla del curso**: siempre activa el entorno virtual antes de trabajar.
> Si instalas librerías sin activarlo, las instalas globalmente y eventualmente tendrás conflictos.

### requirements.txt — la lista de dependencias

```bash
# Guardar las dependencias instaladas en un archivo
pip freeze > requirements.txt

# El archivo se verá así:
# requests==2.31.0
# pydantic==2.5.0
# fastapi==0.109.0

# Instalar todas las dependencias de un proyecto existente
pip install -r requirements.txt
```

**Flujo normal al clonar un proyecto del diplomado:**
```bash
git clone git@github.com:usuario/ia-dev-template.git
cd ia-dev-template
python3 -m venv .venv
source .venv/bin/activate        # (o el equivalente en tu OS)
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

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

## Práctica final — Prepara el entorno del diplomado

Antes de continuar al Nivel 2, verifica que puedes hacer esto:

```bash
# 1. Clona el repositorio del diplomado
git clone git@github.com:[URL-del-instructor]/ia-dev-template.git
cd ia-dev-template

# 2. Crea y activa el entorno virtual
python3 -m venv .venv
source .venv/bin/activate    # (.venv\Scripts\activate en Windows)

# 3. Instala las dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configura las variables de entorno
cp .env.example .env
# Abre .env y agrega: MOCK_MODE=true

# 5. Verifica que los tests pasan
pytest -q
# Debe mostrar algo como: 3 passed in 0.45s

# 6. Inicia el servidor
uvicorn app.main:app --reload
# Abre http://localhost:8000/docs en el navegador
# Debes ver la documentación de la API
```

Si todos los pasos funcionan → estás listo/a para el Nivel 2 y para la primera clase.

---

*Continúa con* → `python_essentials.md` (Nivel 2)
