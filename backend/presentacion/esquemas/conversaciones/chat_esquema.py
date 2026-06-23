from pydantic import BaseModel


class ChatMensajeEntradaEsquema(BaseModel):
    contenido: str


class ChatMensajeRespuestaEsquema(BaseModel):
    id: str
    conversacion_id: str
    rol: str
    contenido: str
    tipo_respuesta: str | None

    model_config = {"from_attributes": True}