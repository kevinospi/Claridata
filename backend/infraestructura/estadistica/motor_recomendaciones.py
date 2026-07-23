from infraestructura.estadistica.dto_descubrimientos import (
    ResultadoMotorDescubrimientos,
    SeveridadDescubrimiento,
    TipoDescubrimiento,
)
from infraestructura.estadistica.dto_interpretacion_profesional import (
    ResultadoMotorInterpretacion,
    TipoSeccionInterpretacion,
)
from infraestructura.estadistica.dto_recomendaciones import (
    PrioridadRecomendacion,
    Recomendacion,
    ResultadoMotorRecomendaciones,
)
from infraestructura.estadistica.dto_resultados import ResultadoMotorEstadistico


_UMBRAL_ASIMETRIA_FUERTE = 1.0
_UMBRAL_CV_ALTA = 1.0
_UMBRAL_FALTANTES_CRITICO = 0.30
_UMBRAL_FALTANTES_MODERADO = 0.05
_UMBRAL_CORRELACION_ALTA = 0.8
_UMBRAL_OUTLIERS_MUCHOS = 0.15
_MIN_FILAS_MODELO = 30



def _recomendar_mediana(
    estadistico: ResultadoMotorEstadistico,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []

    for dist in estadistico.distribuciones:
        if abs(dist.asimetria) >= _UMBRAL_ASIMETRIA_FUERTE:
            est = next(
                (e for e in estadistico.estadisticas_descriptivas
                 if e.columna == dist.columna),
                None,
            )
            if est is None:
                continue

            diferencia_pct = (
                abs(est.media - est.mediana) / max(abs(est.media), 0.001)
            ) * 100

            recomendaciones.append(
                Recomendacion(
                    titulo=f"Usar mediana como medida central en '{dist.columna}'",
                    categoria="Estadística descriptiva",
                    prioridad=PrioridadRecomendacion.ALTA,
                    razon=(
                        f"La variable '{dist.columna}' presenta asimetría fuerte "
                        f"({dist.asimetria:.2f}). La media ({est.media:,.2f}) y la "
                        f"mediana ({est.mediana:,.2f}) difieren en un {diferencia_pct:.1f}%, "
                        "lo que indica que la media está siendo distorsionada por valores extremos."
                    ),
                    accion=(
                        f"Reportar la mediana ({est.mediana:,.2f}) como medida de "
                        "tendencia central en lugar de la media para esta variable. "
                        "Considerar también el rango intercuartílico (IQR) como "
                        "medida de dispersión en lugar de la desviación estándar."
                    ),
                )
            )

    return recomendaciones


def _recomendar_media(
    estadistico: ResultadoMotorEstadistico,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []

    for dist in estadistico.distribuciones:
        if abs(dist.asimetria) < 0.5:
            est = next(
                (e for e in estadistico.estadisticas_descriptivas
                 if e.columna == dist.columna),
                None,
            )
            if est is None:
                continue

            recomendaciones.append(
                Recomendacion(
                    titulo=f"La media es apropiada para '{dist.columna}'",
                    categoria="Estadística descriptiva",
                    prioridad=PrioridadRecomendacion.BAJA,
                    razon=(
                        f"La variable '{dist.columna}' presenta distribución "
                        f"aproximadamente simétrica (asimetría: {dist.asimetria:.2f}). "
                        f"La media ({est.media:,.2f}) y la mediana ({est.mediana:,.2f}) "
                        "son similares, indicando ausencia de sesgo significativo."
                    ),
                    accion=(
                        "Puede usar la media como medida de tendencia central con "
                        "confianza. Los métodos estadísticos que asumen normalidad "
                        "son aplicables a esta variable."
                    ),
                )
            )

    return recomendaciones


def _recomendar_outliers(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []
    total_filas = estadistico.metadatos.numero_filas

    for outlier in estadistico.outliers:
        if total_filas == 0 or outlier.cantidad_outliers == 0:
            continue

        proporcion = outlier.cantidad_outliers / total_filas

        if proporcion >= _UMBRAL_OUTLIERS_MUCHOS:
            recomendaciones.append(
                Recomendacion(
                    titulo=f"Investigar y tratar outliers en '{outlier.columna}'",
                    categoria="Calidad de datos",
                    prioridad=PrioridadRecomendacion.ALTA,
                    razon=(
                        f"La variable '{outlier.columna}' contiene "
                        f"{outlier.cantidad_outliers} valores atípicos "
                        f"({proporcion * 100:.1f}% de los registros). "
                        f"Los límites IQR son [{outlier.limite_inferior:,.2f}, "
                        f"{outlier.limite_superior:,.2f}]. Una proporción tan alta "
                        "indica que estos valores podrían ser fenómenos reales "
                        "del dominio o errores sistemáticos de captura."
                    ),
                    accion=(
                        "1. Verificar si los outliers son errores de captura o datos válidos. "
                        "2. Si son errores: corregirlos o eliminarlos. "
                        "3. Si son válidos: aplicar transformación logarítmica o usar "
                        "modelos robustos a outliers (ej. regresión con Huber loss). "
                        "4. Documentar la decisión tomada para reproducibilidad."
                    ),
                )
            )
        elif outlier.cantidad_outliers > 0:
            recomendaciones.append(
                Recomendacion(
                    titulo=f"Revisar valores atípicos en '{outlier.columna}'",
                    categoria="Calidad de datos",
                    prioridad=PrioridadRecomendacion.MEDIA,
                    razon=(
                        f"La variable '{outlier.columna}' contiene "
                        f"{outlier.cantidad_outliers} valor(es) atípico(s) "
                        f"({proporcion * 100:.1f}% de los registros). "
                        "Su impacto sobre la media puede ser moderado."
                    ),
                    accion=(
                        "Inspeccionar manualmente estos valores para determinar "
                        "si son errores o casos excepcionales legítimos. "
                        "Si se van a incluir en modelos, evaluar el uso de "
                        "la mediana en lugar de la media para esta variable."
                    ),
                )
            )

    return recomendaciones


def _recomendar_visualizacion(
    estadistico: ResultadoMotorEstadistico,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []

    vars_numericas = estadistico.clasificacion_variables.numericas
    vars_categoricas = estadistico.clasificacion_variables.categoricas

    if len(vars_numericas) >= 2:
        recomendaciones.append(
            Recomendacion(
                titulo="Explorar relaciones con matriz de dispersión",
                categoria="Visualización",
                prioridad=PrioridadRecomendacion.MEDIA,
                razon=(
                    f"El dataset tiene {len(vars_numericas)} variables numéricas. "
                    "Una matriz de dispersión (scatter plot matrix) permite identificar "
                    "relaciones no lineales que el coeficiente de correlación de Pearson "
                    "podría no capturar."
                ),
                accion=(
                    "Generar un gráfico de pares (pair plot) incluyendo todas las "
                    f"variables numéricas: {', '.join(vars_numericas[:5])}. "
                    "Colorear por variable categórica si existe alguna relevante."
                ),
            )
        )

    for dist in estadistico.distribuciones:
        if abs(dist.asimetria) >= _UMBRAL_ASIMETRIA_FUERTE:
            recomendaciones.append(
                Recomendacion(
                    titulo=f"Visualizar distribución de '{dist.columna}'",
                    categoria="Visualización",
                    prioridad=PrioridadRecomendacion.MEDIA,
                    razon=(
                        f"La asimetría de '{dist.columna}' ({dist.asimetria:.2f}) "
                        "sugiere una distribución con cola pronunciada que conviene "
                        "visualizar para comunicar el hallazgo claramente."
                    ),
                    accion=(
                        f"Generar un histograma o boxplot de '{dist.columna}' "
                        "marcando la media y la mediana como líneas verticales "
                        "para ilustrar visualmente la diferencia entre ambas."
                    ),
                )
            )

    if vars_categoricas and vars_numericas:
        recomendaciones.append(
            Recomendacion(
                titulo="Analizar distribución por categorías",
                categoria="Visualización",
                prioridad=PrioridadRecomendacion.BAJA,
                razon=(
                    f"El dataset combina {len(vars_categoricas)} variable(s) "
                    f"categórica(s) y {len(vars_numericas)} numérica(s). "
                    "Comparar las distribuciones numéricas segmentadas por categoría "
                    "puede revelar diferencias importantes entre grupos."
                ),
                accion=(
                    f"Generar boxplots de las variables numéricas ({', '.join(vars_numericas[:3])}) "
                    f"agrupados por cada variable categórica ({', '.join(vars_categoricas[:2])}). "
                    "Un violin plot es especialmente útil cuando hay muchos registros por grupo."
                ),
            )
        )

    return recomendaciones


def _recomendar_transformacion(
    estadistico: ResultadoMotorEstadistico,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []

    for dist in estadistico.distribuciones:
        if abs(dist.asimetria) >= _UMBRAL_ASIMETRIA_FUERTE:
            est = next(
                (e for e in estadistico.estadisticas_descriptivas
                 if e.columna == dist.columna),
                None,
            )
            if est is None or est.minimo < 0:
                continue

            tipo_transformacion = "logarítmica" if dist.asimetria > 0 else "potencia"
            recomendaciones.append(
                Recomendacion(
                    titulo=f"Aplicar transformación {tipo_transformacion} a '{dist.columna}'",
                    categoria="Transformación estadística",
                    prioridad=PrioridadRecomendacion.MEDIA,
                    razon=(
                        f"La asimetría de '{dist.columna}' ({dist.asimetria:.2f}) "
                        "viola el supuesto de normalidad requerido por modelos como "
                        "regresión lineal, ANOVA y t-test. Una transformación puede "
                        "acercar la distribución a la normal."
                    ),
                    accion=(
                        f"Aplicar transformación {tipo_transformacion} (log(x+1) si hay ceros) "
                        f"a la variable '{dist.columna}'. "
                        "Verificar después de la transformación si la asimetría se redujo "
                        "a un rango aceptable (|asimetría| < 0.5). "
                        "Alternativamente, explorar transformación Box-Cox con optimización de λ."
                    ),
                )
            )

    if len(estadistico.clasificacion_variables.numericas) >= 3:
        recomendaciones.append(
            Recomendacion(
                titulo="Evaluar normalización de variables numéricas",
                categoria="Transformación estadística",
                prioridad=PrioridadRecomendacion.BAJA,
                razon=(
                    f"El dataset tiene {len(estadistico.clasificacion_variables.numericas)} "
                    "variables numéricas con posiblemente distintas escalas. "
                    "Muchos algoritmos de machine learning son sensibles a diferencias "
                    "de escala entre variables."
                ),
                accion=(
                    "Aplicar StandardScaler (z-score) si se van a usar modelos basados "
                    "en distancias o gradientes (SVM, K-NN, redes neuronales, regresión). "
                    "Aplicar MinMaxScaler si se requiere un rango fijo [0,1]. "
                    "Los modelos basados en árboles (Random Forest, XGBoost) no requieren "
                    "normalización."
                ),
            )
        )

    return recomendaciones


def _recomendar_calidad(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []
    total_filas = estadistico.metadatos.numero_filas

    faltantes_criticos = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.VALORES_FALTANTES
        and d.severidad == SeveridadDescubrimiento.CRITICO
    ]

    faltantes_moderados = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.VALORES_FALTANTES
        and d.severidad != SeveridadDescubrimiento.CRITICO
    ]

    if faltantes_criticos:
        columnas = ", ".join(f"'{d.columna}'" for d in faltantes_criticos)
        recomendaciones.append(
            Recomendacion(
                titulo="Decidir estrategia para columnas con muchos faltantes",
                categoria="Calidad de datos",
                prioridad=PrioridadRecomendacion.ALTA,
                razon=(
                    f"Las columnas {columnas} superan el 30% de valores faltantes. "
                    "Incluirlas sin tratamiento puede sesgar significativamente "
                    "cualquier análisis o modelo entrenado con estos datos."
                ),
                accion=(
                    "Evaluar tres alternativas para cada columna afectada: "
                    "1. Eliminar la columna si no es esencial para el análisis. "
                    "2. Imputar con la mediana (numéricas) o moda (categóricas) "
                    "si los faltantes son aleatorios. "
                    "3. Aplicar imputación múltiple (MICE) si los faltantes "
                    "tienen un patrón no aleatorio."
                ),
            )
        )

    if faltantes_moderados:
        recomendaciones.append(
            Recomendacion(
                titulo="Imputar valores faltantes moderados",
                categoria="Calidad de datos",
                prioridad=PrioridadRecomendacion.MEDIA,
                razon=(
                    f"Se detectaron {len(faltantes_moderados)} columna(s) con "
                    "valores faltantes en proporciones bajas o moderadas. "
                    "Una imputación simple es generalmente suficiente en estos casos."
                ),
                accion=(
                    "Para variables numéricas: imputar con la mediana si hay asimetría, "
                    "o con la media si la distribución es simétrica. "
                    "Para variables categóricas: imputar con la moda o crear una "
                    "categoría 'Desconocido' si los faltantes tienen significado propio."
                ),
            )
        )

    constantes = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.VARIABLE_CONSTANTE
    ]
    if constantes:
        columnas_const = ", ".join(f"'{d.columna}'" for d in constantes)
        recomendaciones.append(
            Recomendacion(
                titulo="Eliminar variables constantes del análisis",
                categoria="Calidad de datos",
                prioridad=PrioridadRecomendacion.ALTA,
                razon=(
                    f"Las columnas {columnas_const} tienen el mismo valor en todos "
                    "los registros. No aportan información discriminativa y pueden "
                    "causar errores numéricos en modelos de machine learning."
                ),
                accion=(
                    "Excluir estas columnas del dataset antes de entrenar cualquier "
                    "modelo. Si son columnas de identificación (IDs), separarlas "
                    "como metadatos y no incluirlas como variables predictoras."
                ),
            )
        )

    return recomendaciones


def _recomendar_proximo_analisis(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> list[Recomendacion]:
    recomendaciones: list[Recomendacion] = []
    n_filas = estadistico.metadatos.numero_filas
    n_vars_num = len(estadistico.clasificacion_variables.numericas)

    tiene_correlaciones = (
        estadistico.correlaciones is not None
        and len(estadistico.correlaciones.pares_relevantes) > 0
    )

    if tiene_correlaciones and n_filas >= _MIN_FILAS_MODELO:
        recomendaciones.append(
            Recomendacion(
                titulo="Explorar análisis de regresión",
                categoria="Próximo análisis",
                prioridad=PrioridadRecomendacion.MEDIA,
                razon=(
                    "Se detectaron correlaciones relevantes entre variables numéricas "
                    f"y el dataset tiene {n_filas} registros, suficientes para "
                    "ajustar un modelo de regresión con poder estadístico razonable."
                ),
                accion=(
                    "Identificar la variable dependiente (la que se quiere predecir) "
                    "y construir un modelo de regresión lineal como línea base. "
                    "Evaluar el R² y los residuos para determinar si el modelo "
                    "lineal es apropiado o si se necesita una forma funcional más compleja."
                ),
            )
        )

    if n_vars_num >= 3 and n_filas >= _MIN_FILAS_MODELO:
        recomendaciones.append(
            Recomendacion(
                titulo="Considerar análisis de componentes principales (PCA)",
                categoria="Próximo análisis",
                prioridad=PrioridadRecomendacion.BAJA,
                razon=(
                    f"Con {n_vars_num} variables numéricas, un análisis PCA puede "
                    "revelar la estructura subyacente de los datos y reducir la "
                    "dimensionalidad manteniendo la mayor parte de la varianza."
                ),
                accion=(
                    "Aplicar PCA sobre las variables numéricas (previa estandarización). "
                    "Graficar la varianza explicada acumulada para determinar cuántos "
                    "componentes son suficientes. Un punto de codo en la curva indica "
                    "el número óptimo de componentes."
                ),
            )
        )

    if n_filas >= _MIN_FILAS_MODELO:
        recomendaciones.append(
            Recomendacion(
                titulo="Explorar segmentación con clustering",
                categoria="Próximo análisis",
                prioridad=PrioridadRecomendacion.BAJA,
                razon=(
                    "El dataset tiene suficientes registros para aplicar algoritmos "
                    "de clustering no supervisado que podrían revelar grupos naturales "
                    "en los datos."
                ),
                accion=(
                    "Aplicar K-Means con k=2..5 sobre las variables numéricas "
                    "estandarizadas. Usar el método del codo o el índice de silueta "
                    "para determinar el número óptimo de clusters. "
                    "Validar que los clusters tienen interpretación en el dominio del problema."
                ),
            )
        )
    else:
        recomendaciones.append(
            Recomendacion(
                titulo="Ampliar el dataset antes de modelar",
                categoria="Próximo análisis",
                prioridad=PrioridadRecomendacion.ALTA,
                razon=(
                    f"El dataset tiene solo {n_filas} registros. La mayoría de los "
                    "algoritmos de machine learning requieren al menos 30 registros "
                    "para producir resultados estadísticamente válidos."
                ),
                accion=(
                    "Recopilar más datos antes de proceder con modelado predictivo. "
                    "Con el tamaño actual, limitar el análisis a estadística descriptiva "
                    "y visualizaciones exploratorias."
                ),
            )
        )

    return recomendaciones



class MotorRecomendacionesInteligentes:
    """
    Motor de Recomendaciones Inteligentes de Claridata.

    Recibe ResultadoMotorEstadistico, ResultadoMotorDescubrimientos y
    ResultadoMotorInterpretacion para generar recomendaciones estructuradas
    y priorizadas para el analista.

    Principios:
    - Nunca recalcula estadísticas.
    - Nunca accede al dataset directamente.
    - Completamente determinístico.
    - Desacoplado de todos los motores anteriores.
    - La interfaz es estable para futura integración con LLM.
    """

    def recomendar(
        self,
        estadistico: ResultadoMotorEstadistico,
        descubrimientos: ResultadoMotorDescubrimientos,
        interpretacion: ResultadoMotorInterpretacion,
    ) -> ResultadoMotorRecomendaciones:
        resultado = ResultadoMotorRecomendaciones()

        for r in _recomendar_mediana(estadistico):
            resultado.agregar(r)

        for r in _recomendar_media(estadistico):
            resultado.agregar(r)

        for r in _recomendar_outliers(estadistico, descubrimientos):
            resultado.agregar(r)

        for r in _recomendar_visualizacion(estadistico):
            resultado.agregar(r)

        for r in _recomendar_transformacion(estadistico):
            resultado.agregar(r)

        for r in _recomendar_calidad(estadistico, descubrimientos):
            resultado.agregar(r)

        for r in _recomendar_proximo_analisis(estadistico, descubrimientos):
            resultado.agregar(r)

        return resultado