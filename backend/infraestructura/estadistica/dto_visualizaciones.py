from dataclasses import dataclass, field
from enum import Enum


class TipoVisualizacion(str, Enum):
    HISTOGRAMA = "HISTOGRAMA"
    BOXPLOT = "BOXPLOT"
    SCATTER = "SCATTER"
    HEATMAP = "HEATMAP"
    BARRAS = "BARRAS"
    DISTRIBUCION = "DISTRIBUCION"


class PrioridadVisualizacion(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"


@dataclass
class Visualizacion:
    tipo: TipoVisualizacion
    titulo: str
    descripcion: str
    prioridad: PrioridadVisualizacion
    motivo: str
    variables: list[str] = field(default_factory=list)
    configuracion: dict = field(default_factory=dict)

    def como_dict(self) -> dict:
        return {
            "tipo": self.tipo.value,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad.value,
            "motivo": self.motivo,
            "variables": self.variables,
            "configuracion": self.configuracion,
        }


@dataclass
class ResultadoMotorVisualizaciones:
    visualizaciones: list[Visualizacion] = field(default_factory=list)

    def agregar(self, visualizacion: Visualizacion) -> None:
        self.visualizaciones.append(visualizacion)

    def como_lista_dict(self) -> list[dict]:
        orden = {
            PrioridadVisualizacion.ALTA: 0,
            PrioridadVisualizacion.MEDIA: 1,
            PrioridadVisualizacion.BAJA: 2,
        }
        return [
            v.como_dict()
            for v in sorted(
                self.visualizaciones,
                key=lambda v: orden[v.prioridad],
            )
        ]