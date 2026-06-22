import numpy as np
import pandas as pd

from infraestructura.estadistica.dto_resultados import (
    ClasificacionVariables,
    EstadisticasColumnaNumerica,
    MetadatosDataset,
    ParCorrelacionRelevante,
    ResultadoCorrelaciones,
    ResultadoDistribucionColumna,
    ResultadoMotorEstadistico,
    ResultadoOutliersColumna,
    ValoresNulos,
)
from infraestructura.estadistica.lector_dataset import LectorDataset

UMBRAL_CORRELACION_RELEVANTE = 0.7
MULTIPLICADOR_IQR = 1.5


class MotorEstadistico:
    def __init__(self, lector_dataset: LectorDataset | None = None) -> None:
        self._lector_dataset = lector_dataset or LectorDataset()

    def analizar(self, ruta_archivo: str, tipo_archivo: str) -> ResultadoMotorEstadistico:
        dataframe = self._lector_dataset.leer(ruta_archivo, tipo_archivo)
        return self.analizar_dataframe(dataframe)

    def analizar_dataframe(self, dataframe: pd.DataFrame) -> ResultadoMotorEstadistico:
        metadatos = self._calcular_metadatos(dataframe)
        valores_nulos = self._calcular_valores_nulos(dataframe)
        clasificacion = self._clasificar_variables(dataframe)
        estadisticas = self._calcular_estadisticas_descriptivas(dataframe, clasificacion.numericas)
        correlaciones = self._calcular_correlaciones(dataframe, clasificacion.numericas)
        outliers = self._detectar_outliers(dataframe, clasificacion.numericas)
        distribuciones = self._calcular_distribuciones(dataframe, clasificacion.numericas)

        return ResultadoMotorEstadistico(
            metadatos=metadatos,
            valores_nulos=valores_nulos,
            clasificacion_variables=clasificacion,
            estadisticas_descriptivas=estadisticas,
            correlaciones=correlaciones,
            outliers=outliers,
            distribuciones=distribuciones,
        )

    def _calcular_metadatos(self, dataframe: pd.DataFrame) -> MetadatosDataset:
        return MetadatosDataset(
            numero_filas=int(dataframe.shape[0]),
            numero_columnas=int(dataframe.shape[1]),
            nombres_columnas=list(dataframe.columns.astype(str)),
            tipos_datos={
                str(columna): str(dtype) for columna, dtype in dataframe.dtypes.items()
            },
        )

    def _calcular_valores_nulos(self, dataframe: pd.DataFrame) -> ValoresNulos:
        nulos_por_columna = dataframe.isnull().sum()
        return ValoresNulos(
            por_columna={
                str(columna): int(cantidad) for columna, cantidad in nulos_por_columna.items()
            },
            total=int(nulos_por_columna.sum()),
        )

    def _clasificar_variables(self, dataframe: pd.DataFrame) -> ClasificacionVariables:
        numericas = list(dataframe.select_dtypes(include=[np.number]).columns.astype(str))
        categoricas = [
            str(columna) for columna in dataframe.columns if str(columna) not in numericas
        ]
        return ClasificacionVariables(numericas=numericas, categoricas=categoricas)

    def _calcular_estadisticas_descriptivas(
        self,
        dataframe: pd.DataFrame,
        columnas_numericas: list[str],
    ) -> list[EstadisticasColumnaNumerica]:
        resultados: list[EstadisticasColumnaNumerica] = []

        for columna in columnas_numericas:
            serie = dataframe[columna].dropna()

            if serie.empty:
                continue

            resultados.append(
                EstadisticasColumnaNumerica(
                    columna=columna,
                    media=float(serie.mean()),
                    mediana=float(serie.median()),
                    desviacion_estandar=float(serie.std()) if len(serie) > 1 else 0.0,
                    minimo=float(serie.min()),
                    maximo=float(serie.max()),
                )
            )

        return resultados

    def _calcular_correlaciones(
        self,
        dataframe: pd.DataFrame,
        columnas_numericas: list[str],
    ) -> ResultadoCorrelaciones | None:
        if len(columnas_numericas) < 2:
            return None

        matriz_df = dataframe[columnas_numericas].corr(method="pearson")

        matriz: dict[str, dict[str, float]] = {
            columna_a: {
                columna_b: self._normalizar_float(matriz_df.loc[columna_a, columna_b])
                for columna_b in columnas_numericas
            }
            for columna_a in columnas_numericas
        }

        pares_relevantes: list[ParCorrelacionRelevante] = []
        for i, columna_a in enumerate(columnas_numericas):
            for columna_b in columnas_numericas[i + 1 :]:
                coeficiente = matriz[columna_a][columna_b]
                if abs(coeficiente) >= UMBRAL_CORRELACION_RELEVANTE:
                    pares_relevantes.append(
                        ParCorrelacionRelevante(
                            columna_a=columna_a,
                            columna_b=columna_b,
                            coeficiente=coeficiente,
                        )
                    )

        return ResultadoCorrelaciones(
            matriz=matriz,
            pares_relevantes=pares_relevantes,
            umbral_relevancia=UMBRAL_CORRELACION_RELEVANTE,
        )

    def _detectar_outliers(
        self,
        dataframe: pd.DataFrame,
        columnas_numericas: list[str],
    ) -> list[ResultadoOutliersColumna]:
        resultados: list[ResultadoOutliersColumna] = []

        for columna in columnas_numericas:
            serie = dataframe[columna].dropna()

            if serie.empty:
                continue

            q1 = float(serie.quantile(0.25))
            q3 = float(serie.quantile(0.75))
            iqr = q3 - q1
            limite_inferior = q1 - MULTIPLICADOR_IQR * iqr
            limite_superior = q3 + MULTIPLICADOR_IQR * iqr

            cantidad_outliers = int(
                ((serie < limite_inferior) | (serie > limite_superior)).sum()
            )

            resultados.append(
                ResultadoOutliersColumna(
                    columna=columna,
                    q1=q1,
                    q3=q3,
                    iqr=iqr,
                    limite_inferior=limite_inferior,
                    limite_superior=limite_superior,
                    cantidad_outliers=cantidad_outliers,
                )
            )

        return resultados

    def _calcular_distribuciones(
        self,
        dataframe: pd.DataFrame,
        columnas_numericas: list[str],
    ) -> list[ResultadoDistribucionColumna]:
        resultados: list[ResultadoDistribucionColumna] = []

        for columna in columnas_numericas:
            serie = dataframe[columna].dropna()

            if len(serie) < 3:
                continue

            asimetria = serie.skew()
            curtosis_valor = serie.kurt()

            resultados.append(
                ResultadoDistribucionColumna(
                    columna=columna,
                    asimetria=self._normalizar_float(asimetria),
                    curtosis=self._normalizar_float(curtosis_valor),
                )
            )

        return resultados

    def _normalizar_float(self, valor: float) -> float:
        if pd.isna(valor):
            return 0.0
        return float(valor)