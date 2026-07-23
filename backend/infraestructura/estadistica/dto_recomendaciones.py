from dataclasses import dataclass, field
from enum import Enum


class PrioridadRecomendacion(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"


@dataclass
class Recomendacion:
    titulo: str
    categoria: str
    prioridad: PrioridadRecomendacion
    razon: str
    accion: str

    def como_dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "categoria": self.categoria,
            "prioridad": self.prioridad.value,
            "razon": self.razon,
            "accion": self.accion,
        }


@dataclass
class ResultadoMotorRecomendaciones:
    recomendaciones: list[Recomendacion] = field(default_factory=list)

    def agregar(self, recomendacion: Recomendacion) -> None:
        self.recomendaciones.append(recomendacion)

    def como_lista_dict(self) -> list[dict]:
        orden = {
            PrioridadRecomendacion.ALTA: 0,
            PrioridadRecomendacion.MEDIA: 1,
            PrioridadRecomendacion.BAJA: 2,
        }
        ordenadas = sorted(
            self.recomendaciones,
            key=lambda r: orden[r.prioridad],
        )
        return [r.como_dict() for r in ordenadas]