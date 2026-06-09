# frontend/app.py
import os

import httpx
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="AI Software Engineering - Diplomado",
    page_icon="🤖",
    layout="wide",
)

# Configuración del entorno (busca la variable o usa localhost por defecto)
# Esto es clave para que funcione tanto en Docker como en local
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def check_backend_health() -> dict[str, str] | None:
    """Verifica si el backend está respondiendo."""
    try:
        response = httpx.get(f"{BACKEND_URL}/health", timeout=2.0)
        if response.status_code == 200:
            return response.json()
        return None
    except httpx.HTTPError:
        return None


# --- UI Principal ---
st.title("🤖 AI Software Engineer Workbench")
st.markdown(f"**Backend URL:** `{BACKEND_URL}`")

# Sidebar de estado
with st.sidebar:
    st.header("Estado del Sistema")
    health = check_backend_health()
    if health:
        st.success(f"Backend Online (v{health['version']})")
    else:
        st.error("Backend Offline 🔴")
        st.warning("Asegúrate de ejecutar: `uv run uvicorn app.main:app --reload`")

# Tabs para organizar las tareas del curso
tab1, tab2, tab3 = st.tabs(["🏠 Home", "🛠️ M1: SDLC Tools", "🕵️ M4: Agentes"])

with tab1:
    st.markdown(
        """
    ### Bienvenido al Template del Curso
    Este entorno está configurado para:
    1.  **Conectarse a una API FastAPI** (ver sidebar).
    2.  **Ejecutar flujos de IA** (próximamente).
    3.  **Visualizar datos** y prototipos.

    #### Instrucciones rápidas:
    - Edita `app/main.py` para agregar lógica.
    - Edita `frontend/app.py` para cambiar esta interfaz.
    """
    )

with tab2:
    st.info("Aquí construiremos las herramientas del Módulo 1 (Generador de Specs, etc.)")

with tab3:
    st.info("Aquí vivirán los Agentes Autónomos del Módulo 4.")
