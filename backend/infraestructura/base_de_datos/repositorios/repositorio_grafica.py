from sqlalchemy.orm import Session

from infraestructura.base_de_datos.modelos.grafica_modelo import GraficaModelo
from infraestructura.base_de_datos.repositorios.repositorio_base import RepositorioBase


class RepositorioGrafica(RepositorioBase[GraficaModelo]):
    def __init__(self, sesion: Session) -> None:
        super().__init__(sesion, GraficaModelo)

    def obtener_por_informe(self, informe_id: str) -> list[GraficaModelo]:
        return list(
            self._sesion.query(GraficaModelo)
            .filter(GraficaModelo.informe_id == informe_id)
            .all()
        )