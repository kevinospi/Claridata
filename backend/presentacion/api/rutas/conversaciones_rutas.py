from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.conversaciones.crear_conversacion import CrearConversacion
from aplicacion.casos_de_uso.conversaciones.obtener_conversacion import ObtenerConversacion
from aplicacion.casos_de_uso.conversaciones.listar_conversaciones_por_informe import (
    ListarConversacionesPorInforme,
)
from aplicacion.casos_de_uso.conversaciones.listar_conversaciones_aprendizaje_usuario import (
    ListarConversacionesAprendizajeUsuario,
)
from aplicacion.casos_de_uso.conversaciones.eliminar_conversacion import EliminarConversacion
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_conversacion
from presentacion.api.dependencias.dependencias_usuario import obtener_usuario_actual_id
from presentacion.esquemas.conversaciones.conversacion_esquema import (
    ConversacionCreacionEsquema,
    ConversacionRespuestaEsquema,
)

router = APIRouter()


@router.post(
    "/conversaciones",
    response_model=ConversacionRespuestaEsquema,
    status_code=201,
    tags=["Conversaciones"],
)
def crear_conversacion(
    datos: ConversacionCreacionEsquema,
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> ConversacionRespuestaEsquema:
    caso_de_uso = CrearConversacion(repositorio_conversacion)
    conversacion = caso_de_uso.ejecutar(
        usuario_id=usuario_id,
        tipo_conversacion=datos.tipo_conversacion,
        informe_id=datos.informe_id,
    )
    return ConversacionRespuestaEsquema.model_validate(conversacion)


@router.get(
    "/conversaciones/aprendizaje",
    response_model=list[ConversacionRespuestaEsquema],
    tags=["Conversaciones"],
)
def listar_conversaciones_aprendizaje(
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> list[ConversacionRespuestaEsquema]:
    caso_de_uso = ListarConversacionesAprendizajeUsuario(repositorio_conversacion)
    conversaciones = caso_de_uso.ejecutar(usuario_id)
    return [ConversacionRespuestaEsquema.model_validate(c) for c in conversaciones]


@router.get(
    "/conversaciones/informe/{informe_id}",
    response_model=list[ConversacionRespuestaEsquema],
    tags=["Conversaciones"],
)
def listar_conversaciones_por_informe(
    informe_id: str,
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
) -> list[ConversacionRespuestaEsquema]:
    caso_de_uso = ListarConversacionesPorInforme(repositorio_conversacion)
    conversaciones = caso_de_uso.ejecutar(informe_id)
    return [ConversacionRespuestaEsquema.model_validate(c) for c in conversaciones]


@router.get(
    "/conversaciones/{conversacion_id}",
    response_model=ConversacionRespuestaEsquema,
    tags=["Conversaciones"],
)
def obtener_conversacion(
    conversacion_id: str,
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
) -> ConversacionRespuestaEsquema:
    caso_de_uso = ObtenerConversacion(repositorio_conversacion)
    conversacion = caso_de_uso.ejecutar(conversacion_id)
    return ConversacionRespuestaEsquema.model_validate(conversacion)


@router.delete(
    "/conversaciones/{conversacion_id}",
    status_code=204,
    tags=["Conversaciones"],
)
def eliminar_conversacion(
    conversacion_id: str,
    repositorio_conversacion: RepositorioConversacion = Depends(obtener_repositorio_conversacion),
) -> None:
    caso_de_uso = EliminarConversacion(repositorio_conversacion)
    caso_de_uso.ejecutar(conversacion_id)