from dataclasses import dataclass, field


@dataclass
class EstadisticasColumnaNumerica:
    columna: str
    media: float
    mediana: float
    desviacion_estandar: float
    minimo: float
    maximo: float


@dataclass
class ValoresNulos:
    por_columna: dict[str, int]
    total: int


@dataclass
class MetadatosDataset:
    numero_filas: int
    numero_columnas: int
    nombres_columnas: list[str]
    tipos_datos: dict[str, str]


@dataclass
class ClasificacionVariables:
    numericas: list[str]
    categoricas: list[str]


@dataclass
class ParCorrelacionRelevante:
    columna_a: str
    columna_b: str
    coeficiente: float


@dataclass
class ResultadoCorrelaciones:
    matriz: dict[str, dict[str, float]]
    pares_relevantes: list[ParCorrelacionRelevante]
    umbral_relevancia: float


@dataclass
class ResultadoOutliersColumna:
    columna: str
    q1: float
    q3: float
    iqr: float
    limite_inferior: float
    limite_superior: float
    cantidad_outliers: int


@dataclass
class ResultadoDistribucionColumna:
    columna: str
    asimetria: float
    curtosis: float


@dataclass
class ResultadoMotorEstadistico:
    metadatos: MetadatosDataset
    valores_nulos: ValoresNulos
    clasificacion_variables: ClasificacionVariables
    estadisticas_descriptivas: list[EstadisticasColumnaNumerica] = field(default_factory=list)
    correlaciones: ResultadoCorrelaciones | None = None
    outliers: list[ResultadoOutliersColumna] = field(default_factory=list)
    distribuciones: list[ResultadoDistribucionColumna] = field(default_factory=list)