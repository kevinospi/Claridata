from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infraestructura.configuracion.settings import obtener_settings

settings = obtener_settings()

app = FastAPI(
    title=settings.app_name,
    description="Plataforma de análisis estadístico asistida por inteligencia artificial.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Sistema"])
def verificar_estado() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}