from datetime import datetime

from pydantic import BaseModel


class MensajeRespuestaEsquema(BaseModel):
    id: str
    conversacion_id: str
    rol: str
    contenido: str
    tipo_respuesta: str | None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}


class MensajeCreacionEsquema(BaseModel):
    rol: str
    contenido: str
    tipo_respuesta: str | None = None