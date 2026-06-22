from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.mensajes.crear_mensaje import CrearMensaje
from aplicacion.casos_de_uso.mensajes.listar_mensajes_conversacion import (
    ListarMensajesConversacion,
)
from aplicacion.casos_de_uso.mensajes.eliminar_mensaje import EliminarMensaje
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_mensaje
from presentacion.esquemas.mensajes.mensaje_esquema import (
    MensajeCreacionEsquema,
    MensajeRespuestaEsquema,
)

router = APIRouter()


@router.post(
    "/conversaciones/{conversacion_id}/mensajes",
    response_model=MensajeRespuestaEsquema,
    status_code=201,
    tags=["Mensajes"],
)
def crear_mensaje(
    conversacion_id: str,
    datos: MensajeCreacionEsquema,
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
) -> MensajeRespuestaEsquema:
    caso_de_uso = CrearMensaje(repositorio_mensaje)
    mensaje = caso_de_uso.ejecutar(
        conversacion_id=conversacion_id,
        rol=datos.rol,
        contenido=datos.contenido,
        tipo_respuesta=datos.tipo_respuesta,
    )
    return MensajeRespuestaEsquema.model_validate(mensaje)


@router.get(
    "/conversaciones/{conversacion_id}/mensajes",
    response_model=list[MensajeRespuestaEsquema],
    tags=["Mensajes"],
)
def listar_mensajes(
    conversacion_id: str,
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
) -> list[MensajeRespuestaEsquema]:
    caso_de_uso = ListarMensajesConversacion(repositorio_mensaje)
    mensajes = caso_de_uso.ejecutar(conversacion_id)
    return [MensajeRespuestaEsquema.model_validate(m) for m in mensajes]


@router.delete(
    "/mensajes/{mensaje_id}",
    status_code=204,
    tags=["Mensajes"],
)
def eliminar_mensaje(
    mensaje_id: str,
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
) -> None:
    caso_de_uso = EliminarMensaje(repositorio_mensaje)
    caso_de_uso.ejecutar(mensaje_id)