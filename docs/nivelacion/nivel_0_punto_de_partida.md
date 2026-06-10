# Nivel 0 — Punto de Partida Absoluto

> **Para quién**: no tenés experiencia en programación, o venís de otro lenguaje
> y el ecosistema Python/terminal te es completamente ajeno.
>
> **Meta**: poder completar el Lab 0 antes de arrancar con el contenido del diplomado.

---

## Parte 1 — La terminal: tu nueva herramienta principal

### ¿Qué es la terminal?

La terminal (también llamada consola, shell, o línea de comandos) es una forma de hablarle a tu computadora escribiendo instrucciones de texto, en lugar de hacer clic en íconos. Los programadores la usan todo el tiempo porque permite hacer cosas que las interfaces gráficas no tienen, y porque se puede automatizar.

### Cómo abrir la terminal

**macOS:**
1. Presiona `Cmd + Espacio` para abrir Spotlight
2. Escribe "Terminal" y presiona Enter
3. También puedes ir a Aplicaciones → Utilidades → Terminal

**Windows — opción A: PowerShell**
1. Presiona `Win + R`, escribe `powershell`, presiona Enter
2. O busca "PowerShell" en el menú Inicio

**Windows — opción B: WSL2 (recomendado para el diplomado)**
WSL2 te da una terminal Linux dentro de Windows. Es la opción más compatible con el curso.
- Instrucciones de instalación: [docs.microsoft.com/es-es/windows/wsl/install](https://docs.microsoft.com/es-es/windows/wsl/install)
- Comando rápido (en PowerShell como administrador): `wsl --install`
- Reinicia, y se abrirá Ubuntu automáticamente

**Linux:**
- Busca "Terminal" en tu lanzador de aplicaciones
- O usa el atajo `Ctrl + Alt + T` en Ubuntu/Mint

### Comandos básicos de terminal — los que más usarás

```bash
# Ver en qué carpeta estás (print working directory)
pwd

# Ver qué archivos hay en la carpeta actual
ls          # Mac/Linux
dir         # Windows PowerShell

# Entrar a una carpeta (change directory)
cd nombre-de-carpeta

# Volver una carpeta atrás
cd ..

# Crear una carpeta nueva
mkdir mi-proyecto

# Ver el contenido de un archivo de texto
cat archivo.txt      # Mac/Linux
type archivo.txt     # Windows

# Limpiar la pantalla
clear       # Mac/Linux
cls         # Windows
```

**Practica esto**: abre la terminal y navega hasta tu escritorio:
```bash
cd ~/Desktop        # Mac/Linux
cd $HOME\Desktop    # Windows PowerShell
pwd                 # verifica que llegaste
```

> 💡 **Consejo**: la terminal recuerda comandos anteriores. Presiona la flecha ↑ para repetir el último comando. Presiona `Tab` para auto-completar nombres de carpetas y archivos.

---

## Parte 2 — Instalar Python

### Verificar si ya tienes Python

Abre la terminal y escribe:
```bash
python3 --version
```

Si ves algo como `Python 3.12.3`, ya tenés Python instalado. **Verificá que sea 3.12.x exacto** (no 3.11, no 3.13 — el diplomado fija esta versión para garantizar reproducibilidad). Si tenés cualquier otra versión, seguí las instrucciones de instalación abajo.

Si ves `command not found` (o un error similar), necesitas instalarlo.

### Instalar Python

**macOS:**
```bash
# Primero instala Homebrew si no lo tienes
# (Homebrew es el gestor de paquetes estándar en Mac)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Luego instala Python
brew install python@3.12

# Verifica
python3 --version
```

**Windows:**
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descargá Python 3.12 (versión exacta — el diplomado no soporta 3.11 ni 3.13)
3. **Importante**: durante la instalación, marca la casilla "Add Python to PATH"
4. Completa la instalación
5. Abre una nueva ventana de PowerShell y verifica: `python --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
python3 --version
```

---

## Parte 3 — Conceptos básicos de Python

### Variables

Una variable guarda un valor con un nombre.

```python
# Crea un archivo llamado intro.py y escribe esto:
nombre = "Ana"
edad = 28
precio = 49.99
activo = True

# Imprime los valores
print(nombre)      # Ana
print(edad)        # 28
print(tipo)        # no existe → error (esto es intencional)
```

Para ejecutar el archivo:
```bash
python3 intro.py
```

¿Viste un error con `tipo`? Eso es un **NameError** — Python no puede usar una variable que no definiste. Los errores son normales. Lee el mensaje: dice exactamente qué pasó y en qué línea.

### Tipos de datos básicos

```python
# Texto (str)
mensaje = "Hola mundo"
otro = 'También funciona con comillas simples'

# Número entero (int)
cantidad = 42

# Número decimal (float)
precio = 3.14

# Verdadero/Falso (bool)
aprobado = True
rechazado = False

# Nada / ausencia de valor (None)
resultado = None
```

### Listas — colecciones ordenadas

```python
# Una lista puede tener cualquier tipo de dato
frutas = ["manzana", "pera", "naranja"]
numeros = [1, 2, 3, 4, 5]
mixto = ["texto", 42, True]

# Acceder a un elemento (el índice empieza en 0)
print(frutas[0])    # manzana
print(frutas[1])    # pera
print(frutas[-1])   # naranja (el último, con índice negativo)

# Agregar un elemento
frutas.append("mango")
print(frutas)       # ['manzana', 'pera', 'naranja', 'mango']

# Ver cuántos elementos tiene
print(len(frutas))  # 4
```

### Diccionarios — colecciones con clave y valor

Los diccionarios son la estructura más importante para el diplomado.
Representan información organizada por nombre, no por posición.

```python
# Un diccionario tiene claves (str) y valores (cualquier tipo)
usuario = {
    "nombre": "Ana",
    "edad": 28,
    "activo": True
}

# Acceder a un valor por su clave
print(usuario["nombre"])    # Ana
print(usuario["edad"])      # 28

# Agregar o modificar un valor
usuario["email"] = "ana@ejemplo.com"
usuario["edad"] = 29

# Verificar si una clave existe
if "email" in usuario:
    print("Tiene email:", usuario["email"])

# Iterar sobre un diccionario
for clave, valor in usuario.items():
    print(f"{clave}: {valor}")
```

### Funciones

```python
# Definir una función
def saludar(nombre):
    mensaje = f"Hola, {nombre}!"
    return mensaje

# Llamar a la función
resultado = saludar("Ana")
print(resultado)    # Hola, Ana!

# Función con múltiples parámetros y valor por defecto
def crear_usuario(nombre, activo=True):
    return {
        "nombre": nombre,
        "activo": activo
    }

usuario1 = crear_usuario("Ana")              # activo=True por defecto
usuario2 = crear_usuario("Bob", activo=False)
print(usuario1)    # {'nombre': 'Ana', 'activo': True}
print(usuario2)    # {'nombre': 'Bob', 'activo': False}
```

### Bucles

```python
# Recorrer una lista
frutas = ["manzana", "pera", "naranja"]
for fruta in frutas:
    print(fruta)

# Recorrer un rango de números
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

# Mientras una condición sea verdadera
contador = 0
while contador < 3:
    print(f"Contador: {contador}")
    contador = contador + 1
```

### Condicionales

```python
nota = 75

if nota >= 90:
    print("Sobresaliente")
elif nota >= 70:
    print("Aprobado")
else:
    print("Reprobado")
```

---

## Parte 4 — Qué es JSON

JSON (JavaScript Object Notation) es el formato estándar para enviar datos entre aplicaciones en internet. Aunque el nombre dice "JavaScript", se usa en todos los lenguajes.

### JSON se parece a los diccionarios de Python

```json
{
  "nombre": "Ana",
  "edad": 28,
  "activo": true,
  "cursos": ["Python", "Docker", "Git"],
  "direccion": {
    "ciudad": "Santiago",
    "pais": "Chile"
  }
}
```

Las diferencias con Python:
- En JSON, `true`/`false` van en minúsculas (en Python es `True`/`False`)
- En JSON, el equivalente a `None` es `null`
- Las claves siempre deben ir entre comillas dobles `"clave"` (Python acepta sin comillas dentro del dict)

### Python puede convertir entre dict y JSON

```python
import json

# Dict de Python → texto JSON
usuario = {"nombre": "Ana", "edad": 28}
texto_json = json.dumps(usuario)
print(texto_json)         # {"nombre": "Ana", "edad": 28}
print(type(texto_json))   # <class 'str'> — es texto

# Texto JSON → dict de Python
datos_json = '{"nombre": "Bob", "activo": true}'
diccionario = json.loads(datos_json)
print(diccionario["nombre"])    # Bob
print(type(diccionario))        # <class 'dict'>
```

---

## Parte 5 — Qué es HTTP y cómo funciona una API

### HTTP: el idioma de internet

Cuando abres una página web, tu navegador envía una **solicitud HTTP** al servidor. El servidor responde con el contenido. Esto pasa miles de veces mientras navegas.

Las APIs usan el mismo mecanismo, pero en lugar de páginas HTML, intercambian datos en JSON.

### Anatomía de una solicitud HTTP

```
GET /usuarios/42 HTTP/1.1
Host: api.ejemplo.com
Authorization: Bearer mi-token-secreto
```

Partes:
- **Método** (`GET`): qué quieres hacer
- **Ruta** (`/usuarios/42`): a qué recurso
- **Headers** (`Authorization`): información adicional

### Los métodos HTTP más comunes

| Método | Propósito | Ejemplo |
|--------|-----------|---------|
| `GET` | Obtener información | Listar usuarios, ver un pedido |
| `POST` | Crear algo nuevo | Registrar un usuario, enviar un formulario |
| `PUT` | Reemplazar algo | Actualizar todos los datos de un perfil |
| `PATCH` | Modificar parcialmente | Cambiar solo el email de un perfil |
| `DELETE` | Eliminar algo | Borrar una cuenta |

### Status codes: qué responde el servidor

| Código | Significa | Cuándo ocurre |
|--------|-----------|---------------|
| `200 OK` | Todo bien | La solicitud funcionó |
| `201 Created` | Creado | Se creó el recurso (después de POST) |
| `400 Bad Request` | Error del cliente | Mandaste datos incorrectos |
| `401 Unauthorized` | No autenticado | No enviaste credenciales |
| `403 Forbidden` | No autorizado | Tus credenciales no tienen permiso |
| `404 Not Found` | No existe | El recurso no existe |
| `422 Unprocessable Entity` | Datos inválidos | Los datos no pasaron validación |
| `500 Internal Server Error` | Error del servidor | El servidor tuvo un problema |

### Tu primera llamada a una API real

La API de JSONPlaceholder existe para practicar — es gratuita y no requiere registro.

```python
# Instala requests si no lo tienes: pip install requests
import requests

# Obtener una lista de usuarios
respuesta = requests.get("https://jsonplaceholder.typicode.com/users")

# Ver el status code
print(respuesta.status_code)    # 200

# Ver los datos en JSON
datos = respuesta.json()        # convierte a lista de dicts
primer_usuario = datos[0]
print(primer_usuario["name"])   # Leanne Graham
print(primer_usuario["email"])  # Sincere@april.biz

# Obtener un recurso específico
respuesta2 = requests.get("https://jsonplaceholder.typicode.com/users/1")
usuario = respuesta2.json()
print(usuario)                  # dict con el usuario #1
```

---

## Parte 6 — Git básico: guardar y compartir tu código

Git es el sistema que permite guardar versiones de tu código y colaborar con otras personas. GitHub es el sitio donde se almacenan esas versiones en la nube.

### Instalar Git

**macOS**: `brew install git`
**Windows**: descarga desde [git-scm.com](https://git-scm.com) — incluye Git Bash
**Linux**: `sudo apt install git`

Verificar:
```bash
git --version
```

### Configuración inicial (solo una vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Flujo básico: clonar → modificar → guardar

```bash
# 1. Copiar un repositorio de GitHub a tu máquina
git clone https://github.com/usuario/repositorio.git

# 2. Entrar a la carpeta
cd repositorio

# 3. Ver qué archivos cambiaste
git status

# 4. Agregar los cambios para guardar
git add nombre-del-archivo.py
# o agregar todo:
git add .

# 5. Guardar los cambios con un mensaje
git commit -m "Agrego la función de validación de email"

# 6. Enviar los cambios a GitHub
git push
```

### Clonar el repositorio del Lab 0

El flujo del diplomado pasa por **GitHub Classroom**: en Moodle, vas a tener un enlace de invitación para el Lab 0. Cuando hagas click, GitHub te crea automáticamente un repositorio privado bajo tu cuenta con el template del curso.

Una vez aceptada la invitación, andá a tu repo en GitHub, click en el botón verde **Code**, copiás la URL HTTPS, y en tu terminal:

```bash
git clone https://github.com/<tu-usuario>/lab-0-<tu-usuario>.git
cd lab-0-<tu-usuario>
```

La primera vez que pushees vas a necesitar autenticarte. GitHub eliminó las contraseñas — usá un **Personal Access Token (PAT)**:

1. Andá a [github.com/settings/tokens](https://github.com/settings/tokens) → *Generate new token (classic)*
2. Marcá los permisos `repo` y `workflow`
3. Copiá el token y usalo como password cuando git te lo pida

> **SSH es una alternativa más avanzada** (no requiere PAT, pero hay que generar y registrar una clave). Si ya sabés usar SSH o querés aprender, hay tutoriales en `docs/nivelacion/03_git_github_guide.md` dentro del repo del Lab.

---

## Práctica final — Mini proyecto para verificar que avanzaste

Completa esto antes de pasar al Nivel 1:

```python
# Crea un archivo llamado practica_nivel0.py

# 1. Define una función que reciba un nombre y una edad
#    y retorne un diccionario con esos datos
def crear_persona(nombre, edad):
    # tu código aquí
    pass

# 2. Crea una lista con 3 personas usando tu función
personas = [
    crear_persona("Ana", 28),
    crear_persona("Bob", 35),
    crear_persona("Carla", 22),
]

# 3. Imprime solo los nombres de las personas mayores de 25 años
for persona in personas:
    # tu código aquí
    pass

# 4. Convierte la lista a JSON e imprímela
import json
# tu código aquí
```

Ejecuta con: `python3 practica_nivel0.py`

Si tu código corre sin errores y muestra los nombres correctos + el JSON → estás listo/a para el Nivel 1.

---

## Recursos adicionales (en español)

- [Python para todos — py4e.com/book](https://es.py4e.com/book) — libro gratuito, excelente para principiantes
- [W3Schools Python](https://www.w3schools.com/python/) — referencia rápida con ejemplos interactivos
- [Aprende Git con juego visual](https://learngitbranching.js.org/?locale=es_ES) — para entender branching visualmente

---

*Continúa con* → `nivel_1_python_y_web_basico.md`
