from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from aplicacion.excepciones import UsuarioNoEncontradoError


class ObtenerUsuarioPorId:
    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        self._repositorio_usuario = repositorio_usuario

    def ejecutar(self, usuario_id: str) -> UsuarioModelo:
        usuario = self._repositorio_usuario.obtener_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe un usuario con id '{usuario_id}'.")
        return usuario