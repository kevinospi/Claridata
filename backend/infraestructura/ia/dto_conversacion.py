from dataclasses import dataclass, field


@dataclass
class MensajeContexto:
    rol: str
    contenido: str


@dataclass
class ContextoInforme:
    resumen_ejecutivo: str | None
    conclusiones: str | None
    hallazgos_principales: dict | None
    recomendaciones: dict | None
    correlaciones: dict | None = None
    deteccion_outliers: dict | None = None
    analisis_distribucion: dict | None = None
    historial: list[MensajeContexto] = field(default_factory=list)


@dataclass
class RespuestaConversacional:
    contenido: str
    tipo_respuesta: str = "estandar"