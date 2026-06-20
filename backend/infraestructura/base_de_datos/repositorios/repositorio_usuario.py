from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioUsuario(RepositorioBase[UsuarioModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, UsuarioModelo)

    def obtener_por_email(self, email: str) -> UsuarioModelo | None:
        return (
            self._sesion.query(UsuarioModelo)
            .filter(UsuarioModelo.email == email)
            .first()
        )