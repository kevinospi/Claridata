from dataclasses import dataclass, field
from enum import Enum


class TipoSeccionInterpretacion(str, Enum):
    RESUMEN_GENERAL = "RESUMEN_GENERAL"
    VARIABLES_DESTACADAS = "VARIABLES_DESTACADAS"
    PATRONES_DETECTADOS = "PATRONES_DETECTADOS"
    CALIDAD_DATOS = "CALIDAD_DATOS"
    RELACIONES_ENCONTRADAS = "RELACIONES_ENCONTRADAS"
    IMPLICACIONES = "IMPLICACIONES"
    RECOMENDACIONES_ANALITICAS = "RECOMENDACIONES_ANALITICAS"


@dataclass
class SeccionInterpretacion:
    tipo: TipoSeccionInterpretacion
    titulo: str
    parrafos: list[str] = field(default_factory=list)

    def agregar_parrafo(self, texto: str) -> None:
        parrafo_limpio = texto.strip()
        if parrafo_limpio:
            self.parrafos.append(parrafo_limpio)

    def tiene_contenido(self) -> bool:
        return bool(self.parrafos)

    def como_dict(self) -> dict:
        return {
            "tipo": self.tipo.value,
            "titulo": self.titulo,
            "parrafos": self.parrafos,
        }


@dataclass
class ResultadoMotorInterpretacion:
    secciones: list[SeccionInterpretacion] = field(default_factory=list)

    def agregar_seccion(self, seccion: SeccionInterpretacion) -> None:
        if seccion.tiene_contenido():
            self.secciones.append(seccion)

    def como_lista_dict(self) -> list[dict]:
        return [s.como_dict() for s in self.secciones]