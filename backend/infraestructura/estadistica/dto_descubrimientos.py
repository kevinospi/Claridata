from dataclasses import dataclass, field
from enum import Enum


class SeveridadDescubrimiento(str, Enum):
    INFORMATIVO = "INFORMATIVO"
    ATENCION = "ATENCION"
    IMPORTANTE = "IMPORTANTE"
    CRITICO = "CRITICO"


class TipoDescubrimiento(str, Enum):
    OUTLIERS = "OUTLIERS"
    ASIMETRIA = "ASIMETRIA"
    CURTOSIS = "CURTOSIS"
    CORRELACION_FUERTE = "CORRELACION_FUERTE"
    CORRELACION_NEGATIVA = "CORRELACION_NEGATIVA"
    VALORES_FALTANTES = "VALORES_FALTANTES"
    VARIABLE_CONSTANTE = "VARIABLE_CONSTANTE"
    ALTA_VARIABILIDAD = "ALTA_VARIABILIDAD"
    BAJA_VARIABILIDAD = "BAJA_VARIABILIDAD"
    DISTRIBUCION_SOSPECHOSA = "DISTRIBUCION_SOSPECHOSA"


@dataclass
class Descubrimiento:
    tipo: TipoDescubrimiento
    titulo: str
    descripcion: str
    severidad: SeveridadDescubrimiento
    columna: str | None = None
    valor: float | None = None
    recomendacion: str | None = None


@dataclass
class ResultadoMotorDescubrimientos:
    descubrimientos: list[Descubrimiento] = field(default_factory=list)

    def agregar(self, descubrimiento: Descubrimiento) -> None:
        self.descubrimientos.append(descubrimiento)

    def como_lista_dict(self) -> list[dict]:
        return [
            {
                "tipo": d.tipo.value,
                "titulo": d.titulo,
                "descripcion": d.descripcion,
                "severidad": d.severidad.value,
                "columna": d.columna,
                "valor": d.valor,
                "recomendacion": d.recomendacion,
            }
            for d in self.descubrimientos
        ]