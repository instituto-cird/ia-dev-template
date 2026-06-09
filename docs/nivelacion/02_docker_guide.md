# Nivelación: Docker para el Diplomado

> **¿Para quién?** Si nunca has escrito un Dockerfile o no entiendes qué hace
> `docker compose up`. Tiempo estimado: 1 hora.
>
> En el diplomado, Docker es obligatorio a partir de M3 para garantizar que
> "funciona en mi máquina" no sea una excusa válida en la defensa.

---

## ¿Qué problema resuelve Docker?

Sin Docker: "En mi máquina funciona, en la del instructor no."
Con Docker: Ambos corren exactamente el mismo ambiente, con las mismas versiones.

Docker empaqueta tu código + su ambiente (Python 3.12, dependencias, variables de entorno)
en una **imagen** reproducible. Cuando corres la imagen, creas un **contenedor**.

---

## Conceptos mínimos

| Término | Analogía | Qué es |
|---|---|---|
| **Imagen** | Receta de cocina | Snapshot del ambiente: OS + Python + código |
| **Contenedor** | Comida preparada | Imagen corriendo como proceso aislado |
| **Dockerfile** | La receta escrita | Instrucciones para construir la imagen |
| **docker-compose** | Menú completo | Orquesta múltiples contenedores juntos |
| **Puerto** | Número de mesa | Mapeo entre el contenedor y tu máquina local |
| **Volumen** | Caja de ingredientes compartida | Carpeta compartida entre host y contenedor |

---

## Anatomy del Dockerfile.backend

```dockerfile
# Base: imagen oficial de Python 3.12 sin extras innecesarios
FROM python:3.12-slim

# Copia uv desde su imagen oficial (más rápido que instalarlo vía pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# PRIMERO copia solo los archivos de dependencias (aprovecha el cache)
# Si solo cambia el código fuente, Docker no reinstala paquetes
COPY pyproject.toml uv.lock ./

# Instala dependencias (sin dev tools — producción)
RUN uv sync --frozen --no-dev

# DESPUÉS copia el código fuente
COPY app/ ./app/

# Puerto que el contenedor expone (documentación — no lo abre en el host)
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**¿Por qué `COPY pyproject.toml uv.lock` antes que `COPY app/`?**
Docker construye por capas. Si copias el código antes de instalar dependencias,
cualquier cambio en el código (incluso un comentario) invalida la capa de instalación
y reinstala todo desde cero. Con el orden correcto, solo reinstala si cambias `pyproject.toml`.

---

## docker-compose.yml — Los tres servicios

```bash
# El repo incluye un docker-compose.yml con:
# - backend  (tu API FastAPI)     → localhost:8000
# - frontend (Streamlit)          → localhost:8501
# - mock-llm (simula OpenAI)      → localhost:8001

# Levantar todo
docker compose up --build

# Solo el backend (para desarrollar sin Streamlit)
docker compose up backend --build

# En background (sin bloquear el terminal)
docker compose up -d --build

# Ver logs del backend en tiempo real
docker compose logs -f backend

# Parar todo
docker compose down
```

---

## Comandos esenciales

```bash
# Construir la imagen manualmente (sin compose)
docker build -f Dockerfile.backend -t mi-api:dev .

# Correr el contenedor manualmente
docker run -p 8000:8000 --env-file .env mi-api:dev

# Ver contenedores corriendo
docker ps

# Ver logs de un contenedor
docker logs [container-id-o-nombre]

# Entrar al contenedor (para debugging)
docker exec -it [container-name] /bin/bash

# Eliminar contenedores parados + imágenes sin usar
docker system prune
```

---

## Variables de entorno en Docker

```yaml
# docker-compose.yml — dos formas de pasar variables

# Opción A: archivo .env (recomendada para desarrollo)
services:
  backend:
    env_file:
      - .env          # Lee el archivo .env de tu proyecto

# Opción B: inline (para valores no secretos)
services:
  backend:
    environment:
      - BACKEND_URL=http://backend:8000
      - MOCK_MODE=true
```

> **Importante:** En Docker, los servicios se comunican por nombre, no por `localhost`.
> El frontend se conecta al backend como `http://backend:8000`, no `http://localhost:8000`.
> Esto ya está configurado en el `docker-compose.yml` del repo.

---

## Verificar que funciona correctamente

```bash
# Después de `docker compose up --build`:

# 1. Backend health check
curl http://localhost:8000/health
# Esperado: {"status":"ok","version":"0.1.0","module":"System"}

# 2. Documentación interactiva
# Abre http://localhost:8000/docs en el browser

# 3. Mock LLM
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-mock","messages":[{"role":"user","content":"test"}]}'
# Esperado: respuesta JSON con "choices"

# 4. Frontend
# Abre http://localhost:8501 en el browser
# El sidebar debe mostrar "Backend Online (v0.1.0)"
```

---

## Errores comunes y soluciones

**Error: `connection refused` al hacer curl al backend**
```bash
# El contenedor puede estar todavía iniciando. Espera 10s y reintenta.
# O verifica que el puerto 8000 no está ocupado por otro proceso:
lsof -i :8000
```

**Error: `cannot find module` o `ModuleNotFoundError`**
```bash
# Las dependencias no se instalaron correctamente.
# Borra el cache y reconstruye:
docker compose down
docker compose build --no-cache
docker compose up
```

**Error: `permission denied` en archivos copiados**
```bash
# En Linux/Mac, asegúrate de que los archivos tienen permisos de lectura:
chmod -R 644 app/
```

**Error: backend se conecta a `localhost:8001` en lugar de `mock-llm:8001`**
```bash
# En Docker, `localhost` dentro del contenedor es el propio contenedor.
# Verifica que OPENAI_BASE_URL en .env sea "http://mock-llm:8001/v1"
# (no "http://localhost:8001/v1")
```

---

## Para la defensa (Demo Day)

La demo puede ser con Docker o en local — lo que decidas. Pero si usas Docker,
asegúrate de haberlo probado en una carpeta limpia (sin `.venv` local) antes.

```bash
# Prueba de "ambiente limpio" (lo que experimenta el evaluador)
git clone https://github.com/[org]/[tu-repo].git repo-limpio
cd repo-limpio
cp .env.example .env
docker compose up --build
# Si funciona: listo. Si no: algo falta en tu Dockerfile o docker-compose.yml.
```

---

## Recursos

- [Docker — Get Started](https://docs.docker.com/get-started/)
- [Docker Compose — Overview](https://docs.docker.com/compose/)
- [Best practices: Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
