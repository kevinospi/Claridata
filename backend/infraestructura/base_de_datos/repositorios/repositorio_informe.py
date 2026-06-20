from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioInforme(RepositorioBase[InformeModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, InformeModelo)

    def obtener_por_dataset(self, dataset_id: str) -> InformeModelo | None:
        return (
            self._sesion.query(InformeModelo)
            .filter(InformeModelo.dataset_id == dataset_id)
            .first()
        )

    def obtener_guardados_por_usuario(self, usuario_id: str) -> list[InformeModelo]:
        return list(
            self._sesion.query(InformeModelo)
            .filter(
                InformeModelo.usuario_id == usuario_id,
                InformeModelo.guardado.is_(True),
            )
            .all()
        )