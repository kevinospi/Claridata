from datetime import datetime

from pydantic import BaseModel, EmailStr


class UsuarioRegistroEsquema(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioRespuestaEsquema(BaseModel):
    id: str
    nombre: str
    email: str
    foto_perfil: str | None
    proveedor_autenticacion: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}