# Imagen base oficial de devcontainers de Microsoft con Python 3.12 sobre Debian Bookworm.
# Trae preinstalado: git, sudo, common-utils, usuario `vscode` no-root.
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Instalar uv (Astral) desde la imagen oficial — versión fija para reproducibilidad.
# Copiamos los binarios directamente; no necesitamos otra cosa de esa imagen.
COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /uvx /usr/local/bin/

# Asegurar que el usuario `vscode` puede ejecutar uv y uvx.
RUN chmod +x /usr/local/bin/uv /usr/local/bin/uvx

# Dependencias del sistema que algunos paquetes del stack pueden necesitar.
# Se mantienen al mínimo: el resto lo resuelve uv.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        graphviz \
        libpq-dev \
        make \
        sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configuración por defecto que mejora el comportamiento de uv dentro de Codespaces.
# UV_LINK_MODE=copy evita advertencias cuando el cache vive en otro filesystem.
# UV_COMPILE_BYTECODE=1 reduce el tiempo de arranque después de uv sync.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Volver al usuario no-root.
USER vscode

# Confirmar la versión de uv durante el build (queda registrada en los logs).
RUN uv --version
