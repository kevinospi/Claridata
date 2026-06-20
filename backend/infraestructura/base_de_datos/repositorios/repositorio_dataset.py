from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioDataset(RepositorioBase[DatasetModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, DatasetModelo)

    def obtener_por_usuario(self, usuario_id: str) -> list[DatasetModelo]:
        return list(
            self._sesion.query(DatasetModelo)
            .filter(DatasetModelo.usuario_id == usuario_id)
            .all()
        )