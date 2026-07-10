import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Carga variables de entorno desde .env (no falla si .env no existe)
load_dotenv()


# Metadatos para la documentación automática (OpenAPI)
app = FastAPI(
    title="AI Diplomado API",
    description="API Backend para el Diplomado de IA Aplicada a Ingeniería de Software",
    version="0.1.0",
)

# Configuración de CORS — orígenes explícitos para no romper el spec de browsers.
_default_origins = [
    "http://localhost:8501",  # Streamlit frontend
    "http://localhost:3000",  # React/Vite dev server
    "http://127.0.0.1:8501",
    "http://127.0.0.1:3000",
]
_env_origins = os.getenv("CORS_ORIGINS", "")
_origins = [o.strip() for o in _env_origins.split(",") if o.strip()] or _default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# --- Modelos (Pydantic) ---
class HealthResponse(BaseModel):
    status: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    module: str = Field(..., min_length=1)


# --- Endpoints ---
@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    """Endpoint raíz para verificar que la API respira."""
    return {"message": "Bienvenido a la API del Diplomado AI"}


@app.get("/health", response_model=HealthResponse, tags=["Ops"])
async def health_check() -> HealthResponse:
    """Health check estándar para monitoreo."""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        module="System",
    )
