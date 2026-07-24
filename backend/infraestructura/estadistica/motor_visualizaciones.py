from infraestructura.estadistica.dto_descubrimientos import ResultadoMotorDescubrimientos
from infraestructura.estadistica.dto_interpretacion_profesional import ResultadoMotorInterpretacion
from infraestructura.estadistica.dto_recomendaciones import ResultadoMotorRecomendaciones
from infraestructura.estadistica.dto_resultados import ResultadoMotorEstadistico
from infraestructura.estadistica.dto_visualizaciones import (
    PrioridadVisualizacion,
    ResultadoMotorVisualizaciones,
    TipoVisualizacion,
    Visualizacion,
)

# ─── Umbrales ────────────────────────────────────────────────────────────────

_UMBRAL_ASIMETRIA = 0.5
_UMBRAL_CORRELACION = 0.5
_MAX_CATEGORIAS_BARRAS = 20
_MAX_SCATTER_PARES = 5
_MAX_HISTOGRAMAS = 6
_MAX_BOXPLOTS = 8


# ─── Reglas independientes ───────────────────────────────────────────────────

def _generar_histogramas(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    visualizaciones: list[Visualizacion] = []
    numericas = estadistico.clasificacion_variables.numericas[:_MAX_HISTOGRAMAS]

    for columna in numericas:
        est = next(
            (e for e in estadistico.estadisticas_descriptivas if e.columna == columna),
            None,
        )
        dist = next(
            (d for d in estadistico.distribuciones if d.columna == columna),
            None,
        )
        if est is None:
            continue

        tiene_asimetria = dist is not None and abs(dist.asimetria) >= _UMBRAL_ASIMETRIA
        prioridad = (
            PrioridadVisualizacion.ALTA
            if tiene_asimetria
            else PrioridadVisualizacion.MEDIA
        )

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.HISTOGRAMA,
                titulo=f"Distribución de {columna}",
                descripcion=(
                    f"Aproximación de la distribución de '{columna}' "
                    f"usando los parámetros estadísticos calculados."
                ),
                prioridad=prioridad,
                motivo=(
                    f"Asimetría detectada ({dist.asimetria:.2f})"
                    if tiene_asimetria
                    else "Variable numérica relevante para el análisis"
                ),
                variables=[columna],
                configuracion={
                    "media": est.media,
                    "mediana": est.mediana,
                    "desviacion_estandar": est.desviacion_estandar,
                    "minimo": est.minimo,
                    "maximo": est.maximo,
                    "asimetria": dist.asimetria if dist else 0.0,
                    "curtosis": dist.curtosis if dist else 0.0,
                },
            )
        )

    return visualizaciones


def _generar_boxplots(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    visualizaciones: list[Visualizacion] = []
    columnas_con_outliers = [
        o.columna
        for o in estadistico.outliers
        if o.cantidad_outliers > 0
    ][:_MAX_BOXPLOTS]

    numericas_sin_outliers = [
        c for c in estadistico.clasificacion_variables.numericas
        if c not in columnas_con_outliers
    ]

    for columna in columnas_con_outliers:
        outlier = next(
            (o for o in estadistico.outliers if o.columna == columna), None
        )
        if outlier is None:
            continue

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.BOXPLOT,
                titulo=f"BoxPlot de {columna}",
                descripcion=(
                    f"Diagrama de caja para '{columna}' mostrando "
                    f"{outlier.cantidad_outliers} valor(es) atípico(s)."
                ),
                prioridad=PrioridadVisualizacion.ALTA,
                motivo=f"Se detectaron {outlier.cantidad_outliers} outlier(s) en esta variable",
                variables=[columna],
                configuracion={
                    "q1": outlier.q1,
                    "q3": outlier.q3,
                    "iqr": outlier.iqr,
                    "limite_inferior": outlier.limite_inferior,
                    "limite_superior": outlier.limite_superior,
                    "cantidad_outliers": outlier.cantidad_outliers,
                },
            )
        )

    for columna in numericas_sin_outliers[:3]:
        est = next(
            (e for e in estadistico.estadisticas_descriptivas if e.columna == columna),
            None,
        )
        outlier = next(
            (o for o in estadistico.outliers if o.columna == columna), None
        )
        if est is None or outlier is None:
            continue

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.BOXPLOT,
                titulo=f"BoxPlot de {columna}",
                descripcion=f"Diagrama de caja para '{columna}'.",
                prioridad=PrioridadVisualizacion.BAJA,
                motivo="Variable numérica relevante para el análisis exploratorio",
                variables=[columna],
                configuracion={
                    "q1": outlier.q1,
                    "q3": outlier.q3,
                    "iqr": outlier.iqr,
                    "limite_inferior": outlier.limite_inferior,
                    "limite_superior": outlier.limite_superior,
                    "cantidad_outliers": outlier.cantidad_outliers,
                },
            )
        )

    return visualizaciones


def _generar_scatter(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    if estadistico.correlaciones is None:
        return []

    visualizaciones: list[Visualizacion] = []
    pares = estadistico.correlaciones.pares_relevantes[:_MAX_SCATTER_PARES]

    for par in pares:
        abs_coef = abs(par.coeficiente)
        prioridad = (
            PrioridadVisualizacion.ALTA
            if abs_coef >= 0.8
            else PrioridadVisualizacion.MEDIA
        )
        direccion = "positiva" if par.coeficiente >= 0 else "negativa"

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.SCATTER,
                titulo=f"Scatter: {par.columna_a} vs {par.columna_b}",
                descripcion=(
                    f"Relación {direccion} entre '{par.columna_a}' "
                    f"y '{par.columna_b}' (r = {par.coeficiente:.2f})."
                ),
                prioridad=prioridad,
                motivo=f"Correlación {direccion} de {abs_coef:.2f} detectada",
                variables=[par.columna_a, par.columna_b],
                configuracion={
                    "columna_x": par.columna_a,
                    "columna_y": par.columna_b,
                    "coeficiente": par.coeficiente,
                },
            )
        )

    return visualizaciones


def _generar_heatmap(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    if estadistico.correlaciones is None:
        return []

    numericas = estadistico.clasificacion_variables.numericas
    if len(numericas) < 2:
        return []

    matriz = estadistico.correlaciones.matriz

    return [
        Visualizacion(
            tipo=TipoVisualizacion.HEATMAP,
            titulo="Heatmap de correlaciones",
            descripcion=(
                f"Matriz de correlaciones de Pearson entre las "
                f"{len(numericas)} variables numéricas del dataset."
            ),
            prioridad=PrioridadVisualizacion.ALTA,
            motivo="Permite identificar visualmente todas las relaciones lineales del dataset",
            variables=numericas,
            configuracion={
                "matriz": matriz,
                "variables": numericas,
            },
        )
    ]


def _generar_barras(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    visualizaciones: list[Visualizacion] = []
    categoricas = estadistico.clasificacion_variables.categoricas

    for columna in categoricas:
        nulos = estadistico.valores_nulos.por_columna.get(columna, 0)
        total = estadistico.metadatos.numero_filas
        pct_completo = ((total - nulos) / total * 100) if total > 0 else 0

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.BARRAS,
                titulo=f"Distribución de {columna}",
                descripcion=(
                    f"Frecuencias de la variable categórica '{columna}'. "
                    f"Completitud: {pct_completo:.1f}%."
                ),
                prioridad=PrioridadVisualizacion.MEDIA,
                motivo="Variable categórica — la distribución de frecuencias es la visualización natural",
                variables=[columna],
                configuracion={
                    "columna": columna,
                    "total_registros": total,
                    "valores_faltantes": nulos,
                },
            )
        )

    return visualizaciones


def _generar_distribucion_normal(
    estadistico: ResultadoMotorEstadistico,
) -> list[Visualizacion]:
    visualizaciones: list[Visualizacion] = []

    for dist in estadistico.distribuciones:
        if abs(dist.asimetria) >= _UMBRAL_ASIMETRIA:
            continue

        est = next(
            (e for e in estadistico.estadisticas_descriptivas if e.columna == dist.columna),
            None,
        )
        if est is None:
            continue

        visualizaciones.append(
            Visualizacion(
                tipo=TipoVisualizacion.DISTRIBUCION,
                titulo=f"Curva de distribución: {dist.columna}",
                descripcion=(
                    f"'{dist.columna}' presenta distribución aproximadamente normal "
                    f"(asimetría: {dist.asimetria:.2f}, curtosis: {dist.curtosis:.2f})."
                ),
                prioridad=PrioridadVisualizacion.BAJA,
                motivo="Distribución simétrica compatible con supuesto de normalidad",
                variables=[dist.columna],
                configuracion={
                    "media": est.media,
                    "desviacion_estandar": est.desviacion_estandar,
                    "minimo": est.minimo,
                    "maximo": est.maximo,
                    "asimetria": dist.asimetria,
                    "curtosis": dist.curtosis,
                },
            )
        )

    return visualizaciones


# ─── Orquestador ─────────────────────────────────────────────────────────────

class MotorVisualizaciones:
    """
    Motor de Visualizaciones de Claridata.

    Decide qué visualizaciones son apropiadas para un informe basándose
    exclusivamente en los resultados de los motores anteriores.

    Principios:
    - Nunca accede al dataset.
    - Nunca recalcula estadísticas.
    - Produce representaciones estructuradas, no imágenes.
    - Completamente determinístico.
    """

    def generar(
        self,
        estadistico: ResultadoMotorEstadistico,
        descubrimientos: ResultadoMotorDescubrimientos,
        interpretacion: ResultadoMotorInterpretacion,
        recomendaciones: ResultadoMotorRecomendaciones,
    ) -> ResultadoMotorVisualizaciones:
        resultado = ResultadoMotorVisualizaciones()

        for v in _generar_heatmap(estadistico):
            resultado.agregar(v)

        for v in _generar_histogramas(estadistico):
            resultado.agregar(v)

        for v in _generar_boxplots(estadistico):
            resultado.agregar(v)

        for v in _generar_scatter(estadistico):
            resultado.agregar(v)

        for v in _generar_barras(estadistico):
            resultado.agregar(v)

        for v in _generar_distribucion_normal(estadistico):
            resultado.agregar(v)

        return resultado