from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infraestructura.configuracion.settings import obtener_settings
from presentacion.api.rutas.usuarios_rutas import router as usuarios_router
from presentacion.api.rutas.datasets_rutas import router as datasets_router
from presentacion.api.rutas.informes_rutas import router as informes_router
from presentacion.api.rutas.conversaciones_rutas import router as conversaciones_router
from presentacion.api.rutas.mensajes_rutas import router as mensajes_router
from presentacion.middlewares.manejador_excepciones import registrar_manejadores_excepciones

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

registrar_manejadores_excepciones(app)

app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(datasets_router, prefix="/api/v1")
app.include_router(informes_router, prefix="/api/v1")
app.include_router(conversaciones_router, prefix="/api/v1")
app.include_router(mensajes_router, prefix="/api/v1")


@app.get("/health", tags=["Sistema"])
def verificar_estado() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}