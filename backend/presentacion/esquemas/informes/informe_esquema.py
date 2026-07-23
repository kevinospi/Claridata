from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DescubrimientoEsquema(BaseModel):
    tipo: str
    titulo: str
    descripcion: str
    severidad: str
    columna: str | None = None
    valor: float | None = None
    recomendacion: str | None = None


class InformeRespuestaEsquema(BaseModel):
    id: str
    usuario_id: str
    dataset_id: str
    titulo: str
    guardado: bool
    resumen_ejecutivo: str | None
    estadisticas_descriptivas: dict | None
    analisis_distribucion: dict | None
    correlaciones: dict | None
    deteccion_outliers: dict | None
    hallazgos_principales: dict | None
    recomendaciones: dict | None
    conclusiones: str | None
    descubrimientos: list[dict] | None = None
    interpretacion_profesional: list[dict] | None = None
    recomendaciones_inteligentes: list[dict] | None = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}


class InformeResumenEsquema(BaseModel):
    id: str
    titulo: str
    dataset_id: str
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


class InformeRenombrarEsquema(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)

    @field_validator("titulo")
    @classmethod
    def quitar_espacios_extremos(cls, valor: str) -> str:
        valor_limpio = valor.strip()
        if len(valor_limpio) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres.")
        return valor_limpio
    
class ParrafoInterpretacion(BaseModel):
    tipo: str
    titulo: str
    parrafos: list[str]