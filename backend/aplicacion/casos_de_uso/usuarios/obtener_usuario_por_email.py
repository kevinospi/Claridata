from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from aplicacion.excepciones import UsuarioNoEncontradoError


class ObtenerUsuarioPorEmail:
    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        self._repositorio_usuario = repositorio_usuario

    def ejecutar(self, email: str) -> UsuarioModelo:
        usuario = self._repositorio_usuario.obtener_por_email(email)
        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe un usuario con email '{email}'.")
        return usuario