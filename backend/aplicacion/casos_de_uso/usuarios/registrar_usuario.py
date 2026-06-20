from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from aplicacion.excepciones import EmailYaRegistradoError


class RegistrarUsuario:
    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        self._repositorio_usuario = repositorio_usuario

    def ejecutar(
        self,
        nombre: str,
        email: str,
        password_hash: str | None,
        proveedor_autenticacion: str = "email",
        google_id: str | None = None,
        foto_perfil: str | None = None,
    ) -> UsuarioModelo:
        usuario_existente = self._repositorio_usuario.obtener_por_email(email)
        if usuario_existente is not None:
            raise EmailYaRegistradoError(f"El email '{email}' ya está registrado.")

        nuevo_usuario = UsuarioModelo(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            proveedor_autenticacion=proveedor_autenticacion,
            google_id=google_id,
            foto_perfil=foto_perfil,
        )

        self._repositorio_usuario.crear(nuevo_usuario)
        self._repositorio_usuario.guardar_cambios()
        return nuevo_usuario