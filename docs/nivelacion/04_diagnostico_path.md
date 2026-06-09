# Ruta de Nivelación por Diagnóstico

> Este documento es para ti si completaste (o intentaste completar) el **Lab 0 · The Broken Repo**
> y encontraste dificultades en alguna área. Úsalo como mapa personalizado.
>
> Si no tuviste ningún problema con Lab 0, puedes saltarte esta guía — estás listo para M1.

---

## Cómo usar este documento

1. Identifica en qué bug del Lab 0 tuviste dificultades (o no pudiste resolver).
2. Sigue el plan de nivelación correspondiente.
3. Completa los ejercicios de verificación al final de cada plan.
4. **Antes de Clase 01:** confirma que puedes completar Lab 0 en menos de 30 minutos.

Si el instructor te contactó después del Lab 0 indicando un área específica, búscala directamente en la sección correspondiente.

---

## Mapa de diagnóstico

| Síntoma en Lab 0 | Área débil | Plan de nivelación |
|---|---|---|
| No encontré cómo crear una rama y hacer push | Git/GitHub | [Plan A — Git workflow](#plan-a--git-workflow) |
| No entendí el mensaje de error de pytest | Python / Testing | [Plan B — Python y tests](#plan-b--python-y-tests) |
| No pude leer el error de `uv sync` para identificar el typo | Python / Dependencias | [Plan B — Python y tests](#plan-b--python-y-tests) |
| No entendí qué era el `ci.yml` ni cómo modificarlo | CI/GitHub Actions | [Plan C — CI y GitHub Actions](#plan-c--ci-y-github-actions) |
| No supe instalar Python 3.12 o configurar uv | Ambiente local | [Plan D — Setup de ambiente](#plan-d--setup-de-ambiente) |
| Tardé más de 3 horas en total | Múltiples áreas | [Plan E — Nivelación intensiva](#plan-e--nivelación-intensiva) |
| Completé todo pero no entiendo para qué sirve FastAPI | FastAPI | [Plan F — FastAPI básico](#plan-f--fastapi-básico) |
| No sé qué es Docker ni si lo necesito ya | Docker | [Plan G — Docker básico](#plan-g--docker-básico) |

---

## Plan A — Git workflow

**Síntoma:** Dificultad para crear ramas, hacer commits, abrir un PR.

**Tiempo estimado de nivelación:** 2 horas

### Lectura obligatoria

Lee completo: [docs/nivelacion/03_git_github_guide.md](03_git_github_guide.md)

Pon atención especial en:
- Sección 3: Flujo de trabajo en el diplomado (el ciclo exacto que repetirás)
- Sección 4: Mensajes de commit (los commits son parte de la evaluación)
- Sección 7: El CI de GitHub Actions (entiende qué hace cada paso)

### Ejercicio de verificación

Completa este ejercicio en tu repo antes de Clase 01:

```bash
# 1. Crea una rama nueva
git checkout -b nivelacion/git-test

# 2. Crea un archivo de prueba
echo "# Nivelacion Git OK" > docs/nivelacion/git_test.md

# 3. Commit con mensaje convencional
git add docs/nivelacion/git_test.md
git commit -m "docs: add git nivelacion verification file"

# 4. Pushea la rama
git push origin nivelacion/git-test

# 5. Abre un PR en GitHub con título "Nivelacion: Git workflow test"
# 6. Verifica que el CI corre (aunque falle por ahora, el punto es que dispare)
# 7. Cierra el PR SIN mergear (es solo un test)

# ¿Lo completaste sin buscar ayuda? → Estás listo para M1.
```

---

## Plan B — Python y tests

**Síntoma:** No pude leer un stack trace de pytest, no entiendo type hints,
`uv sync` falló y no supe diagnosticarlo.

**Tiempo estimado de nivelación:** 3 horas

### Lectura obligatoria

Lee completo: [docs/nivelacion/00_python_essentials.md](00_python_essentials.md)

Pon atención especial en:
- Sección 1: Type hints (obligatorios en todo el código del diplomado)
- Sección 2: Pydantic v2 (la columna vertebral de Track A)
- Sección 4: pytest — sintaxis de tests y cómo leer errores

### Cómo leer un error de pytest

```
FAILED tests/test_sanity.py::test_health - AssertionError: assert 'healthy' == 'ok'
│                                           │
│                                           └── Lo que el test esperaba
└── Qué test falló y en qué archivo

# El mensaje te dice:
# - Archivo: tests/test_sanity.py
# - Función: test_health
# - Problema: el código retornó 'healthy' pero el test esperaba 'ok'
# - Fix: busca en app/main.py dónde se retorna el status y cámbialo a 'ok'
```

### Ejercicio de verificación

```python
# Crea el archivo tests/test_nivelacion.py con estos tests
# y haz que todos pasen:

from pydantic import BaseModel, Field, ValidationError
import pytest

class Producto(BaseModel):
    nombre: str
    precio: float = Field(gt=0)
    activo: bool = True

def test_producto_valido() -> None:
    p = Producto(nombre="Laptop", precio=999.99)
    assert p.nombre == "Laptop"
    assert p.activo is True  # valor por defecto

def test_precio_negativo_falla() -> None:
    with pytest.raises(ValidationError):
        Producto(nombre="Test", precio=-10.0)

def test_type_hints() -> None:
    # Esta función debe tener type hints correctos para pasar mypy
    def duplicar(n: int) -> int:
        return n * 2
    assert duplicar(5) == 10

# Cómo correrlos:
# uv run pytest tests/test_nivelacion.py -v
```

Si los tres tests pasan y `uv run mypy tests/test_nivelacion.py --ignore-missing-imports`
no reporta errores: estás listo para M1.

---

## Plan C — CI y GitHub Actions

**Síntoma:** No entendí el archivo `.github/workflows/ci.yml`,
no supe cómo ver el resultado del CI en GitHub, o no entendí
por qué el CI fallaba aunque "en mi máquina funcionaba".

**Tiempo estimado de nivelación:** 1 hora

### Lectura obligatoria

Lee la sección 7 de [docs/nivelacion/03_git_github_guide.md](03_git_github_guide.md):
"El CI de GitHub Actions".

### Anatomía del ci.yml del diplomado

```yaml
# .github/workflows/ci.yml
name: CI                    # Nombre que aparece en la pestaña Actions

on:                         # Cuándo se dispara
  pull_request:             # En cada PR
  push:
    branches: [ main ]      # En cada push a main

jobs:
  test:                     # Nombre del job
    runs-on: ubuntu-latest  # Ambiente: Linux en GitHub

    steps:
      - uses: actions/checkout@v4        # Descarga el código del repo
      - uses: actions/setup-python@v5   # Instala Python 3.12
      - uses: astral-sh/setup-uv@v7     # Instala uv
      - run: uv sync --frozen           # Instala dependencias exactas del uv.lock
      - run: uv run ruff check .        # Linter — falla si hay errores de estilo
      - run: uv run mypy app/           # Type checker — falla si hay errores de tipo
      - run: uv run bandit -r app/      # Security — falla si hay vulnerabilidades
      - run: uv run pytest --cov=app    # Tests — falla si tests fallan o coverage < 60%
```

**La diferencia "local vs CI":**

El error más común es: "en mi máquina funciona pero el CI falla".
Las causas habituales son:

| Causa | Diagnóstico | Fix |
|---|---|---|
| Dependencia instalada localmente pero no en `pyproject.toml` | `uv sync --frozen` falla en CI | Agregar el paquete a `pyproject.toml` con `uv add paquete` |
| Variable de entorno local que no existe en CI | Test asume `os.environ["X"]` | Usar `os.getenv("X", "default")` o configurar la variable en GitHub Secrets |
| Archivo local que no está commiteado | CI no tiene el archivo | `git status` → ver si hay archivos sin trackear |
| Python versión diferente | Comportamiento distinto | `.python-version` fija Python 3.12 para ambos ambientes |

### Ejercicio de verificación

```bash
# Simula el CI localmente (exactamente lo que corre GitHub Actions):
uv sync --frozen --all-groups
uv run ruff check .
uv run mypy app/ --ignore-missing-imports
uv run bandit -r app/ -ll -q
uv run pytest -q --cov=app --cov-fail-under=60

# Si los 5 comandos pasan en verde: tu ambiente local está en sync con el CI.
```

---

## Plan D — Setup de ambiente

**Síntoma:** No pude instalar Python 3.12, uv, o Git correctamente.
El ambiente local no funciona después de clonar el repo.

**Tiempo estimado de nivelación:** 1-2 horas

### Checklist de instalación

```bash
# 1. Git
git --version
# Debe retornar: git version 2.x.x
# Instalación: https://git-scm.com/downloads

# 2. Python 3.12 (uv lo maneja automáticamente)
# No necesitas instalarlo manualmente si instalas uv primero

# 3. uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
# Debe retornar: uv x.x.x

# 4. Clonar y configurar el repo
git clone https://github.com/ia-aplicada-al-desarrollo-de-software/[tu-repo-asignado].git
cd [tu-repo]
uv sync --all-groups    # uv descarga Python 3.12 automáticamente si no está
uv run python --version # Debe retornar: Python 3.12.x

# 5. Verificación completa
uv run pytest tests/test_sanity.py -v
# test_health_status_ok PASSED
# (los demás pueden fallar si el mock LLM no está corriendo — es OK)
```

### Si uv sync falla con un error de red

```bash
# Prueba con --no-cache
uv sync --all-groups --no-cache

# Si estás detrás de un proxy corporativo:
export HTTP_PROXY=http://proxy:puerto
export HTTPS_PROXY=http://proxy:puerto
uv sync --all-groups
```

### Si no tienes permisos para instalar en Windows

Instala con el flag `--user`:
```powershell
# En PowerShell como usuario normal (sin admin)
irm https://astral.sh/uv/install.ps1 | iex
# uv se instala en %APPDATA%\uv\bin — agrega esta carpeta al PATH
```

---

## Plan E — Nivelación intensiva

**Síntoma:** Tardaste más de 3 horas en Lab 0, o no pudiste completarlo.

Esto indica que hay múltiples áreas débiles simultáneamente. El plan recomendado es:

### Semana -2 (antes de Clase 01): 6-8 horas en total

**Día 1 (2h):** Setup de ambiente completo + Git básico
- [Plan D](#plan-d--setup-de-ambiente) completo
- Secciones 1-5 de [docs/nivelacion/03_git_github_guide.md](03_git_github_guide.md)

**Día 2 (2h):** Python esencial
- [docs/nivelacion/00_python_essentials.md](00_python_essentials.md) completo
- Escribir los 3 tests del ejercicio de verificación del Plan B

**Día 3 (2h):** FastAPI básico
- [docs/nivelacion/01_fastapi_guide.md](01_fastapi_guide.md) secciones 1-3
- Agregar un endpoint GET /ping a `app/main.py` con su test

**Día 4 (2h):** CI y primer PR
- Completar el ejercicio de verificación del Plan C
- Abrir un PR real con el endpoint /ping y esperar que el CI corra en verde

### Indicador de readiness para Clase 01

Estás listo si puedes completar esto en menos de 20 minutos:
```bash
git checkout -b feature/readiness-test
# Agrega un endpoint GET /ready que retorne {"ready": true}
# Escribe su test
git add . && git commit -m "feat: add /ready endpoint"
git push origin feature/readiness-test
# Abre PR → espera CI verde → cierra sin mergear
```

---

## Plan F — FastAPI básico

**Síntoma:** Completé Lab 0 pero no entiendo para qué sirve FastAPI,
qué es un endpoint, o qué hace Pydantic.

**Tiempo estimado de nivelación:** 1.5 horas

Lee: [docs/nivelacion/01_fastapi_guide.md](01_fastapi_guide.md) completo.

### Ejercicio de verificación

```python
# Agrega este endpoint a app/main.py y su test a tests/test_sanity.py

# En app/main.py — nuevo modelo y endpoint:
class EchoRequest(BaseModel):
    message: str
    repeat: int = Field(default=1, ge=1, le=10)

class EchoResponse(BaseModel):
    result: str
    times: int

@app.post("/echo", response_model=EchoResponse, tags=["Utils"])
async def echo(body: EchoRequest) -> EchoResponse:
    return EchoResponse(result=body.message * body.repeat, times=body.repeat)

# En tests/test_sanity.py — nuevo test:
def test_echo_endpoint() -> None:
    r = client.post("/echo", json={"message": "hola", "repeat": 3})
    assert r.status_code == 200
    assert r.json()["result"] == "holaholahola"
    assert r.json()["times"] == 3

def test_echo_valida_repeat_maximo() -> None:
    r = client.post("/echo", json={"message": "x", "repeat": 11})  # > 10
    assert r.status_code == 422  # Pydantic lo rechaza automáticamente
```

Si `uv run pytest tests/test_sanity.py -v` pasa con estos dos nuevos tests: listo para M1.

---

## Plan G — Docker básico

**Síntoma:** No sé qué es Docker, no lo tengo instalado,
o no entiendo qué hace `docker compose up`.

**Tiempo estimado de nivelación:** 1 hora

Docker NO es obligatorio hasta M3. Puedes empezar el diplomado sin él.
Pero instálalo ahora para no bloquearte cuando llegue el momento.

Lee: [docs/nivelacion/02_docker_guide.md](02_docker_guide.md) secciones 1-4.

### Ejercicio de verificación (cuando tengas Docker instalado)

```bash
# Construir y correr solo el backend
docker build -f Dockerfile.backend -t ia-dev-backend:test .
docker run -p 8000:8000 --env-file .env ia-dev-backend:test

# En otra terminal:
curl http://localhost:8000/health
# Esperado: {"status":"ok","version":"0.1.0","module":"System"}

# Limpiar
docker stop $(docker ps -q)
docker rmi ia-dev-backend:test
```

Si el `curl` retorna el JSON esperado: tu Dockerfile funciona correctamente.

---

## Después de la nivelación — ¿Cuándo es suficiente?

No necesitas ser experto en todo esto antes de Clase 01.
Necesitas poder hacer esto sin ayuda:

- [ ] Clonar tu repo, correr `uv sync`, correr `pytest`, ver CI verde
- [ ] Crear una rama, hacer un commit con mensaje convencional, pushear, abrir un PR
- [ ] Leer un error de pytest e identificar la línea que falla
- [ ] Correr `ruff check .` y saber qué significa si hay errores

Si puedes hacer esas 4 cosas, estás listo para el diplomado.
El resto lo irás aprendiendo en contexto durante los módulos.

---

## ¿Todavía tienes dudas?

Escribe al canal del diplomado en el Classroom antes de Clase 01.
Incluye:
1. El error exacto que ves (copia y pega el output, no "no funciona")
2. El comando que ejecutaste
3. El OS que estás usando (Windows/Mac/Linux + versión)

> El instructor o un compañero podrán ayudarte más rápido con esa información.
