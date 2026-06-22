from datetime import datetime

from pydantic import BaseModel


class ConversacionRespuestaEsquema(BaseModel):
    id: str
    usuario_id: str
    informe_id: str | None
    tipo_conversacion: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}


class ConversacionCreacionEsquema(BaseModel):
    tipo_conversacion: str
    informe_id: str | None = None