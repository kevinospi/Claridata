from datetime import datetime

from pydantic import BaseModel


class DatasetRespuestaEsquema(BaseModel):
    id: str
    usuario_id: str
    nombre_archivo: str
    tipo_archivo: str
    tamaño_archivo: int
    numero_filas: int | None
    numero_columnas: int | None
    columnas: list | None
    tipos_datos: dict | None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}