from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioMensaje(RepositorioBase[MensajeModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, MensajeModelo)

    def obtener_por_conversacion(self, conversacion_id: str) -> list[MensajeModelo]:
        return list(
            self._sesion.query(MensajeModelo)
            .filter(MensajeModelo.conversacion_id == conversacion_id)
            .order_by(MensajeModelo.fecha_creacion)
            .all()
        )