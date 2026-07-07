# 🐳 Docker Local — Guía Opcional

> **Estado en el curso:** Docker es **opcional** para los Módulos 0 al 3. Aparece como herramienta útil a partir del M2 (servicios externos) y se vuelve recomendable en el M5 (empaquetado del proyecto final).
>
> **Si todavía no lo necesitás, no lo instales aún.** Agregar Docker al stack agrega una capa que puede romperse. Si tu objetivo es cerrar el Lab 0/1, con Python 3.12 + `uv` alcanza.

---

## 📅 ¿Cuándo lo voy a necesitar?

| Módulo | ¿Necesito Docker? | Para qué |
|--------|:-----------------:|----------|
| M0 · Onboarding | ❌ No | El Lab 0 corre con `uv` puro |
| M1 · Fundamentos | ❌ No | El Lab 1 también corre con `uv` puro |
| M2 · Diseño | ⚠️ Útil | Si modelás una base de datos real (Postgres) |
| M3 · Implementación | ⚠️ Útil | Para correr servicios reales en tests de integración |
| M4 · Agentes | ⚠️ Recomendable | Si tu agente consume servicios externos |
| **M5 · Proyecto Final** | ✅ **Recomendable** | Empaquetar tu RC con `docker compose up` es el patrón profesional esperado |

> 🧭 **Atajo:** si llegaste hasta acá porque querés adelantarte para el M5, instalá Docker Desktop ahora y dejalo "esperando". No tenés que aprender Compose esta semana.

---

## 🛠️ Instalación por sistema operativo

### macOS

```bash
# Opción 1 · Descarga oficial (más común)
# https://www.docker.com/products/docker-desktop/  →  descargar Docker Desktop para Mac

# Opción 2 · Homebrew
brew install --cask docker
```

Después de instalar: abrir Docker Desktop una vez para que termine la configuración inicial. Aparece un ícono de ballena 🐳 en la barra superior cuando está corriendo.

### Windows

```powershell
# Requiere Windows 10/11 Pro o WSL2 habilitado
# Descarga: https://www.docker.com/products/docker-desktop/
```

> ⚠️ **WSL2 obligatorio:** si Windows te pide instalar WSL2 antes, seguí las instrucciones. Sin WSL2, Docker Desktop no arranca. Guía oficial: https://learn.microsoft.com/en-us/windows/wsl/install

### Linux (Ubuntu / Debian)

```bash
# Docker Engine (sin Desktop, suficiente para el curso)
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# Permitir usar docker sin sudo (cerrá sesión y volvé a entrar después)
sudo usermod -aG docker $USER
```

### Verificación universal

```bash
docker --version            # debería imprimir 24.x o superior
docker compose version      # debería imprimir 2.x o superior
docker run hello-world      # descarga una imagen mínima y la corre
```

Si los 3 comandos andan, estás listo/a.

---

## 🚀 Comandos básicos que vas a usar en el curso

### 1. Levantar todos los servicios definidos en `docker-compose.yml`

```bash
docker compose up           # en primer plano (logs en consola, Ctrl+C para parar)
docker compose up -d        # en segundo plano (recupera tu terminal)
```

### 2. Ver qué está corriendo

```bash
docker compose ps           # contenedores del compose actual
docker ps                   # TODOS los contenedores en tu máquina
```

### 3. Ver logs

```bash
docker compose logs -f          # todos los servicios, en vivo
docker compose logs -f api      # solo el servicio "api"
```

### 4. Bajar todo

```bash
docker compose down             # apaga los contenedores
docker compose down -v          # apaga + borra los volúmenes (datos perdidos)
```

### 5. Entrar a un contenedor

```bash
docker compose exec api bash    # abre un shell dentro del contenedor "api"
```

---

## 🔥 Troubleshooting de los problemas más frecuentes

### "port is already allocated" / "bind: address already in use"

Algún proceso ya está usando ese puerto en tu máquina (típicamente 5432 si tenés Postgres local, u 8000 si dejaste un FastAPI corriendo).

```bash
# Encontrar quién usa el puerto (ej. 8000)
lsof -i :8000                   # Mac / Linux
netstat -ano | findstr :8000    # Windows

# Soluciones:
# 1. Matar el proceso que lo usa
# 2. Cambiar el puerto en docker-compose.yml (ej. "8001:8000")
```

### Docker Desktop no arranca en Mac (rueda girando)

```bash
# Reiniciar el demonio
killall Docker && open /Applications/Docker.app
```

Si persiste, **resetear a defaults** desde el menú de Docker Desktop (perdés imágenes locales, pero se rebajan rápido).

### "permission denied" en Linux al correr `docker`

Tu usuario no está en el grupo `docker`:

```bash
sudo usermod -aG docker $USER
# Cerrá sesión completamente (logout) y volvé a entrar
```

### El contenedor crashea al arrancar

```bash
docker compose logs <servicio>           # leé los últimos 50 renglones
docker compose logs --tail=100 api       # más historia
```

El 80% de las veces es una **variable de entorno faltante** (`.env` no copiado) o un puerto ya ocupado.

### "no space left on device"

Docker acumula imágenes y volúmenes viejos. Limpiá:

```bash
docker system prune          # borra contenedores parados + imágenes huérfanas
docker system prune -a       # más agresivo: borra TODAS las imágenes no usadas
docker volume prune          # borra volúmenes huérfanos (datos perdidos)
```

---

## 🧠 Conceptos mínimos que conviene entender

**Imagen** — la "receta congelada" de un sistema (ej. `python:3.12-slim`). Se descarga una vez, se reusa muchas.

**Contenedor** — una instancia corriendo de una imagen. Como un proceso ligero. Cuando lo apagás, se borra (salvo lo que vive en un volumen).

**Volumen** — directorio persistente que sobrevive a apagar/borrar contenedores. Acá vive la data de la base de datos, por ejemplo.

**`docker-compose.yml`** — archivo que define varios contenedores juntos (ej. tu API + Postgres + Redis) y cómo se conectan entre sí. `docker compose up` los levanta a todos.

---

## 🎯 Para el Proyecto Final del M5

El estándar profesional esperado es que tu repo incluya:

```yaml
# docker-compose.yml (esqueleto típico)
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: dev
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Y que tu README diga literalmente:

> ```bash
> cp .env.example .env
> docker compose up
> # API corriendo en http://localhost:8000
> ```

Si un evaluador puede clonar tu repo y correr esos 2 comandos sin más fricción, tu Release Candidate aprueba el criterio de "instalación reproducible".

---

## 📚 Para profundizar (opcional)

- 🎥 **Tutorial visual (30 min):** [Docker en 30 minutos · FreeCodeCamp][1] *(en inglés con subtítulos)*
- 📖 **Docs oficiales (referencia):** [docs.docker.com/get-started/][2]
- 📖 **Compose en profundidad:** [docs.docker.com/compose/][3]

---

> 💡 **Última recomendación:** no estudies Docker antes de necesitarlo. Cuando llegues al primer Lab que lo usa, vas a entender los comandos en contexto y se va a fijar mucho mejor. Esta guía está acá para cuando ese momento llegue — no antes.

[1]: https://www.youtube.com/watch?v=fqMOX6JJhGo
[2]: https://docs.docker.com/get-started/
[3]: https://docs.docker.com/compose/
