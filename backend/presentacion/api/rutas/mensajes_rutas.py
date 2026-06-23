from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.mensajes.crear_mensaje import CrearMensaje
from aplicacion.casos_de_uso.mensajes.listar_mensajes_conversacion import (
    ListarMensajesConversacion,
)
from aplicacion.casos_de_uso.mensajes.eliminar_mensaje import EliminarMensaje
from aplicacion.casos_de_uso.conversaciones.responder_mensaje_informe import (
    ResponderMensajeInforme,
)
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from infraestructura.ia.interfaz_interpretador_conversacional import (
    InterpretadorConversacional,
)
from presentacion.api.dependencias.dependencias_db import (
    obtener_interpretador_conversacional,
    obtener_repositorio_conversacion,
    obtener_repositorio_informe,
    obtener_repositorio_mensaje,
)
from presentacion.api.dependencias.dependencias_usuario import obtener_usuario_actual_id
from presentacion.esquemas.conversaciones.chat_esquema import (
    ChatMensajeEntradaEsquema,
    ChatMensajeRespuestaEsquema,
)
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
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> MensajeRespuestaEsquema:
    caso_de_uso = CrearMensaje(repositorio_mensaje, repositorio_conversacion)
    mensaje = caso_de_uso.ejecutar(
        conversacion_id=conversacion_id,
        usuario_id=usuario_id,
        rol=datos.rol,
        contenido=datos.contenido,
        tipo_respuesta=datos.tipo_respuesta,
    )
    return MensajeRespuestaEsquema.model_validate(mensaje)


@router.post(
    "/conversaciones/{conversacion_id}/chat",
    response_model=ChatMensajeRespuestaEsquema,
    status_code=201,
    tags=["Mensajes"],
)
def chat_sobre_informe(
    conversacion_id: str,
    datos: ChatMensajeEntradaEsquema,
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
    interpretador_conversacional: InterpretadorConversacional = Depends(
        obtener_interpretador_conversacional
    ),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> ChatMensajeRespuestaEsquema:
    caso_de_uso = ResponderMensajeInforme(
        repositorio_conversacion,
        repositorio_mensaje,
        repositorio_informe,
        interpretador_conversacional,
    )
    mensaje_asistente = caso_de_uso.ejecutar(
        conversacion_id=conversacion_id,
        usuario_id=usuario_id,
        contenido_mensaje=datos.contenido,
    )
    return ChatMensajeRespuestaEsquema.model_validate(mensaje_asistente)


@router.get(
    "/conversaciones/{conversacion_id}/mensajes",
    response_model=list[MensajeRespuestaEsquema],
    tags=["Mensajes"],
)
def listar_mensajes(
    conversacion_id: str,
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> list[MensajeRespuestaEsquema]:
    caso_de_uso = ListarMensajesConversacion(repositorio_mensaje, repositorio_conversacion)
    mensajes = caso_de_uso.ejecutar(conversacion_id, usuario_id)
    return [MensajeRespuestaEsquema.model_validate(m) for m in mensajes]


@router.delete(
    "/mensajes/{mensaje_id}",
    status_code=204,
    tags=["Mensajes"],
)
def eliminar_mensaje(
    mensaje_id: str,
    repositorio_mensaje: RepositorioMensaje = Depends(obtener_repositorio_mensaje),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> None:
    caso_de_uso = EliminarMensaje(repositorio_mensaje)
    caso_de_uso.ejecutar(mensaje_id, usuario_id)