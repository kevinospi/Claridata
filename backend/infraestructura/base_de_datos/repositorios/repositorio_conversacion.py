from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioConversacion(RepositorioBase[ConversacionModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, ConversacionModelo)

    def obtener_por_informe(self, informe_id: str) -> list[ConversacionModelo]:
        return list(
            self._sesion.query(ConversacionModelo)
            .filter(ConversacionModelo.informe_id == informe_id)
            .all()
        )