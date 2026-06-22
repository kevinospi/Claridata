from datetime import datetime

from pydantic import BaseModel


class InformeRespuestaEsquema(BaseModel):
    id: str
    usuario_id: str
    dataset_id: str
    guardado: bool
    resumen_ejecutivo: str | None
    estadisticas_descriptivas: dict | None
    analisis_distribucion: dict | None
    correlaciones: dict | None
    deteccion_outliers: dict | None
    hallazgos_principales: dict | None
    recomendaciones: dict | None
    conclusiones: str | None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}


class InformeCreacionEsquema(BaseModel):
    dataset_id: str
    resumen_ejecutivo: str | None = None
    estadisticas_descriptivas: dict | None = None
    analisis_distribucion: dict | None = None
    correlaciones: dict | None = None
    deteccion_outliers: dict | None = None
    hallazgos_principales: dict | None = None
    recomendaciones: dict | None = None
    conclusiones: str | None = None