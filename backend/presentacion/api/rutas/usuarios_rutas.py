from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.usuarios.registrar_usuario import RegistrarUsuario
from aplicacion.casos_de_uso.usuarios.obtener_usuario_por_id import ObtenerUsuarioPorId
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_usuario
from presentacion.esquemas.usuarios.usuario_esquema import (
    UsuarioRegistroEsquema,
    UsuarioRespuestaEsquema,
)

router = APIRouter()


@router.post(
    "/auth/registro",
    response_model=UsuarioRespuestaEsquema,
    status_code=201,
    tags=["Usuarios"],
)
def registrar_usuario(
    datos: UsuarioRegistroEsquema,
    repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario),
) -> UsuarioRespuestaEsquema:
    caso_de_uso = RegistrarUsuario(repositorio_usuario)
    usuario = caso_de_uso.ejecutar(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=None,
    )
    return UsuarioRespuestaEsquema.model_validate(usuario)


@router.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioRespuestaEsquema,
    tags=["Usuarios"],
)
def obtener_usuario(
    usuario_id: str,
    repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario),
) -> UsuarioRespuestaEsquema:
    caso_de_uso = ObtenerUsuarioPorId(repositorio_usuario)
    usuario = caso_de_uso.ejecutar(usuario_id)
    return UsuarioRespuestaEsquema.model_validate(usuario)