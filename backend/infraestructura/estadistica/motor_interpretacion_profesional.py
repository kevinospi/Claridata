from infraestructura.estadistica.dto_descubrimientos import (
    ResultadoMotorDescubrimientos,
    SeveridadDescubrimiento,
    TipoDescubrimiento,
)
from infraestructura.estadistica.dto_interpretacion_profesional import (
    ResultadoMotorInterpretacion,
    SeccionInterpretacion,
    TipoSeccionInterpretacion,
)
from infraestructura.estadistica.dto_resultados import ResultadoMotorEstadistico



_UMBRAL_CV_ALTA = 1.0
_UMBRAL_CV_BAJA = 0.05
_UMBRAL_CORRELACION_FUERTE = 0.8
_UMBRAL_ASIMETRIA_FUERTE = 1.0
_UMBRAL_FALTANTES_RELEVANTE = 0.05
_UMBRAL_OUTLIERS_RELEVANTE = 0.05



def _generar_resumen_general(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.RESUMEN_GENERAL,
        titulo="Resumen general del dataset",
    )

    meta = estadistico.metadatos
    n_filas = meta.numero_filas
    n_cols = meta.numero_columnas
    n_num = len(estadistico.clasificacion_variables.numericas)
    n_cat = len(estadistico.clasificacion_variables.categoricas)

    seccion.agregar_parrafo(
        f"El dataset analizado contiene {n_filas:,} registros distribuidos en "
        f"{n_cols} variables: {n_num} numéricas y {n_cat} categóricas."
    )

    total_celdas = n_filas * n_cols
    total_nulos = estadistico.valores_nulos.total
    if total_celdas > 0:
        pct_completo = ((total_celdas - total_nulos) / total_celdas) * 100
        if pct_completo >= 99:
            seccion.agregar_parrafo(
                f"El dataset presenta una completitud del {pct_completo:.1f}%, "
                "lo que indica una calidad de datos excelente para el análisis."
            )
        elif pct_completo >= 90:
            seccion.agregar_parrafo(
                f"El dataset presenta una completitud del {pct_completo:.1f}%. "
                "La mayoría de los registros están completos, aunque existen "
                "algunos valores faltantes que conviene considerar."
            )
        else:
            seccion.agregar_parrafo(
                f"El dataset presenta una completitud del {pct_completo:.1f}%. "
                "La proporción de valores faltantes es significativa y podría "
                "afectar la confiabilidad de las conclusiones."
            )

    criticos = [
        d for d in descubrimientos.descubrimientos
        if d.severidad == SeveridadDescubrimiento.CRITICO
    ]
    importantes = [
        d for d in descubrimientos.descubrimientos
        if d.severidad == SeveridadDescubrimiento.IMPORTANTE
    ]

    if criticos:
        seccion.agregar_parrafo(
            f"El análisis identificó {len(criticos)} hallazgo(s) de severidad crítica "
            "que requieren atención antes de proceder con cualquier modelado o análisis inferencial."
        )
    elif importantes:
        seccion.agregar_parrafo(
            f"El análisis identificó {len(importantes)} hallazgo(s) importantes "
            "que conviene revisar para garantizar la validez de las conclusiones."
        )
    else:
        seccion.agregar_parrafo(
            "No se detectaron problemas críticos en el dataset. "
            "Los datos presentan condiciones adecuadas para continuar el análisis."
        )

    return seccion


def _generar_variables_destacadas(
    estadistico: ResultadoMotorEstadistico,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.VARIABLES_DESTACADAS,
        titulo="Variables con mayor relevancia analítica",
    )

    for est in estadistico.estadisticas_descriptivas:
        if est.media == 0:
            continue

        cv = abs(est.desviacion_estandar / est.media)
        rango = est.maximo - est.minimo

        if cv >= _UMBRAL_CV_ALTA:
            seccion.agregar_parrafo(
                f"La variable '{est.columna}' presenta una dispersión muy elevada "
                f"(coeficiente de variación del {cv * 100:.1f}%), con valores que "
                f"oscilan entre {est.minimo:,.2f} y {est.maximo:,.2f}. "
                "Esta alta variabilidad sugiere heterogeneidad en la población analizada "
                "y merece especial atención antes de aplicar modelos que asuman homogeneidad."
            )
        elif rango > 0 and cv <= _UMBRAL_CV_BAJA:
            seccion.agregar_parrafo(
                f"La variable '{est.columna}' muestra una variabilidad muy baja "
                f"(coeficiente de variación del {cv * 100:.1f}%), con valores "
                f"concentrados alrededor de {est.media:,.2f}. "
                "Su aporte discriminativo en modelos predictivos podría ser limitado."
            )

    if not seccion.tiene_contenido():
        for est in estadistico.estadisticas_descriptivas[:3]:
            seccion.agregar_parrafo(
                f"La variable '{est.columna}' presenta una media de {est.media:,.2f} "
                f"y una desviación estándar de {est.desviacion_estandar:,.2f}, "
                f"con valores entre {est.minimo:,.2f} y {est.maximo:,.2f}."
            )

    return seccion


def _generar_patrones_detectados(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.PATRONES_DETECTADOS,
        titulo="Patrones y comportamientos identificados",
    )

    for dist in estadistico.distribuciones:
        abs_asim = abs(dist.asimetria)
        if abs_asim >= _UMBRAL_ASIMETRIA_FUERTE:
            direccion = "positiva" if dist.asimetria > 0 else "negativa"
            cola = "valores altos extremos" if dist.asimetria > 0 else "valores bajos extremos"
            seccion.agregar_parrafo(
                f"La variable '{dist.columna}' presenta una distribución con asimetría "
                f"{direccion} pronunciada (coeficiente: {dist.asimetria:.2f}), "
                f"lo que indica la presencia de {cola} que separan la media de la mediana. "
                "En este contexto, la mediana es una medida de tendencia central más representativa."
            )
        elif abs_asim < 0.5:
            seccion.agregar_parrafo(
                f"La variable '{dist.columna}' presenta una distribución aproximadamente "
                f"simétrica (asimetría: {dist.asimetria:.2f}), compatible con el supuesto "
                "de normalidad requerido por muchos métodos estadísticos clásicos."
            )

    constantes = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.VARIABLE_CONSTANTE
    ]
    for d in constantes:
        seccion.agregar_parrafo(
            f"La variable '{d.columna}' fue identificada como constante: todos sus registros "
            f"tienen el mismo valor ({d.valor}). Esta variable no aporta variabilidad "
            "al análisis y su inclusión en modelos predictivos podría generar problemas numéricos."
        )

    sospechosas = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.DISTRIBUCION_SOSPECHOSA
    ]
    for d in sospechosas:
        seccion.agregar_parrafo(
            f"La variable '{d.columna}' podría estar representando una categoría "
            "codificada numéricamente. Se recomienda verificar su naturaleza antes "
            "de aplicar operaciones aritméticas sobre ella."
        )

    return seccion


def _generar_calidad_datos(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.CALIDAD_DATOS,
        titulo="Evaluación de calidad de los datos",
    )

    faltantes = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.VALORES_FALTANTES
    ]

    if not faltantes:
        seccion.agregar_parrafo(
            "No se detectaron valores faltantes en el dataset. "
            "La integridad de los datos es completa para todas las variables analizadas."
        )
    else:
        criticos_faltantes = [
            d for d in faltantes
            if d.severidad == SeveridadDescubrimiento.CRITICO
        ]
        if criticos_faltantes:
            nombres = ", ".join(
                f"'{d.columna}'" for d in criticos_faltantes
            )
            seccion.agregar_parrafo(
                f"Las variables {nombres} presentan proporciones críticas de valores "
                "faltantes. Antes de utilizar estas variables en cualquier análisis, "
                "se recomienda evaluar estrategias de imputación o considerar su exclusión."
            )

        moderados = [
            d for d in faltantes
            if d.severidad != SeveridadDescubrimiento.CRITICO
        ]
        if moderados:
            seccion.agregar_parrafo(
                f"Se identificaron {len(moderados)} variable(s) con valores faltantes "
                "en proporciones moderadas. Una imputación por media, mediana o moda "
                "podría ser suficiente dependiendo del contexto del análisis."
            )

    outliers_desc = [
        d for d in descubrimientos.descubrimientos
        if d.tipo == TipoDescubrimiento.OUTLIERS
        and d.severidad in (
            SeveridadDescubrimiento.IMPORTANTE,
            SeveridadDescubrimiento.CRITICO,
        )
    ]
    if outliers_desc:
        cols_outliers = [f"'{d.columna}'" for d in outliers_desc]
        seccion.agregar_parrafo(
            f"Se detectaron valores atípicos significativos en "
            f"{', '.join(cols_outliers)}. "
            "Estos valores pueden distorsionar la media y afectar la estabilidad "
            "de modelos de regresión. Se recomienda tratarlos explícitamente "
            "antes del modelado."
        )

    return seccion


def _generar_relaciones_encontradas(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.RELACIONES_ENCONTRADAS,
        titulo="Relaciones entre variables",
    )

    if estadistico.correlaciones is None:
        return seccion

    pares = estadistico.correlaciones.pares_relevantes
    if not pares:
        seccion.agregar_parrafo(
            "No se identificaron correlaciones lineales relevantes entre las variables "
            "numéricas del dataset (ningún par supera el umbral de relevancia). "
            "Las variables parecen comportarse de forma relativamente independiente."
        )
        return seccion

    pares_positivos = [p for p in pares if p.coeficiente >= _UMBRAL_CORRELACION_FUERTE]
    pares_negativos = [p for p in pares if p.coeficiente <= -_UMBRAL_CORRELACION_FUERTE]
    pares_moderados = [
        p for p in pares
        if -_UMBRAL_CORRELACION_FUERTE < p.coeficiente < _UMBRAL_CORRELACION_FUERTE
    ]

    for par in pares_positivos:
        intensidad = "muy alta" if par.coeficiente >= 0.95 else "alta"
        seccion.agregar_parrafo(
            f"Existe una correlación positiva {intensidad} entre "
            f"'{par.columna_a}' y '{par.columna_b}' (r = {par.coeficiente:.2f}). "
            "A medida que una de estas variables aumenta, la otra tiende a aumentar "
            "de forma proporcional. Esta relación podría indicar redundancia "
            "informativa entre ambas variables."
        )

    for par in pares_negativos:
        seccion.agregar_parrafo(
            f"Existe una correlación negativa fuerte entre "
            f"'{par.columna_a}' y '{par.columna_b}' (r = {par.coeficiente:.2f}). "
            "Cuando una variable aumenta, la otra tiende a disminuir. "
            "Esta relación inversa puede ser de interés analítico o indicar "
            "variables complementarias en el fenómeno estudiado."
        )

    if pares_moderados:
        seccion.agregar_parrafo(
            f"Se identificaron {len(pares_moderados)} par(es) de variables con "
            "correlaciones moderadas que pueden resultar relevantes para análisis "
            "de regresión o segmentación."
        )

    return seccion


def _generar_implicaciones(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.IMPLICACIONES,
        titulo="Implicaciones analíticas",
    )

    tiene_asimetria_fuerte = any(
        abs(d.asimetria) >= _UMBRAL_ASIMETRIA_FUERTE
        for d in estadistico.distribuciones
    )
    if tiene_asimetria_fuerte:
        seccion.agregar_parrafo(
            "La presencia de variables con distribuciones asimétricas sugiere que "
            "los métodos estadísticos que asumen normalidad (como la regresión lineal "
            "ordinaria o el ANOVA) deben aplicarse con cautela. Considerar "
            "transformaciones logarítmicas o el uso de métodos no paramétricos."
        )

    tiene_outliers_criticos = any(
        d.tipo == TipoDescubrimiento.OUTLIERS
        and d.severidad in (
            SeveridadDescubrimiento.IMPORTANTE,
            SeveridadDescubrimiento.CRITICO,
        )
        for d in descubrimientos.descubrimientos
    )
    if tiene_outliers_criticos:
        seccion.agregar_parrafo(
            "Los valores atípicos identificados pueden tener un impacto desproporcionado "
            "sobre modelos sensibles a la escala, como la regresión lineal, los algoritmos "
            "basados en distancias (k-NN, K-Means) o las redes neuronales sin normalización. "
            "Se recomienda aplicar técnicas de robustez o eliminar/transformar estos valores "
            "antes del modelado."
        )

    correlaciones_altas = (
        estadistico.correlaciones is not None
        and any(
            abs(p.coeficiente) >= _UMBRAL_CORRELACION_FUERTE
            for p in estadistico.correlaciones.pares_relevantes
        )
    )
    if correlaciones_altas:
        seccion.agregar_parrafo(
            "La presencia de correlaciones altas entre variables numéricas introduce "
            "riesgo de multicolinealidad en modelos de regresión múltiple, lo que puede "
            "inflar los errores estándar de los coeficientes y dificultar la interpretación "
            "del efecto individual de cada variable."
        )

    tiene_constantes = any(
        d.tipo == TipoDescubrimiento.VARIABLE_CONSTANTE
        for d in descubrimientos.descubrimientos
    )
    if tiene_constantes:
        seccion.agregar_parrafo(
            "Las variables constantes identificadas deben excluirse del análisis predictivo. "
            "Su inclusión puede generar matrices singulares en modelos lineales y "
            "comportamientos indefinidos en algoritmos de machine learning."
        )

    if not seccion.tiene_contenido():
        seccion.agregar_parrafo(
            "El dataset no presenta condiciones que limiten significativamente la "
            "aplicación de métodos estadísticos estándar. Los datos están en condiciones "
            "adecuadas para proceder con análisis exploratorio avanzado o modelado predictivo."
        )

    return seccion


def _generar_recomendaciones(
    estadistico: ResultadoMotorEstadistico,
    descubrimientos: ResultadoMotorDescubrimientos,
) -> SeccionInterpretacion:
    seccion = SeccionInterpretacion(
        tipo=TipoSeccionInterpretacion.RECOMENDACIONES_ANALITICAS,
        titulo="Recomendaciones para el análisis",
    )

    tiene_faltantes = any(
        d.tipo == TipoDescubrimiento.VALORES_FALTANTES
        for d in descubrimientos.descubrimientos
    )
    if tiene_faltantes:
        seccion.agregar_parrafo(
            "Gestionar los valores faltantes antes de continuar: evaluar imputación "
            "por media o mediana para variables numéricas, y por moda para variables "
            "categóricas. En casos con más del 30% de faltantes, considerar la "
            "exclusión de la variable del análisis principal."
        )

    tiene_outliers = any(
        d.tipo == TipoDescubrimiento.OUTLIERS
        for d in descubrimientos.descubrimientos
    )
    if tiene_outliers:
        seccion.agregar_parrafo(
            "Revisar los valores atípicos identificados: determinar si son errores "
            "de captura (y deben corregirse o eliminarse) o fenómenos reales del "
            "dominio (y deben mantenerse o tratarse con técnicas robustas). "
            "Documentar la decisión tomada para garantizar reproducibilidad."
        )

    tiene_asimetria = any(
        abs(d.asimetria) >= _UMBRAL_ASIMETRIA_FUERTE
        for d in estadistico.distribuciones
    )
    if tiene_asimetria:
        seccion.agregar_parrafo(
            "Para las variables con alta asimetría, explorar transformaciones como "
            "logaritmo natural, raíz cuadrada o Box-Cox antes de aplicar modelos "
            "que asuman distribución normal."
        )

    if (
        estadistico.correlaciones is not None
        and estadistico.correlaciones.pares_relevantes
    ):
        seccion.agregar_parrafo(
            "Ante la presencia de correlaciones altas, considerar técnicas de "
            "reducción de dimensionalidad (PCA) o selección de variables antes "
            "del modelado para evitar multicolinealidad."
        )

    n_vars = estadistico.metadatos.numero_columnas
    n_filas = estadistico.metadatos.numero_filas
    if n_filas > 0 and n_vars / n_filas > 0.1:
        seccion.agregar_parrafo(
            "La relación entre el número de variables y el número de registros "
            "es relativamente alta. Se recomienda aplicar técnicas de regularización "
            "o reducción de dimensionalidad si se va a entrenar un modelo predictivo."
        )

    if not seccion.tiene_contenido():
        seccion.agregar_parrafo(
            "El dataset no requiere preprocesamiento especial. Se puede proceder "
            "directamente con análisis exploratorio avanzado, visualizaciones "
            "o construcción de modelos predictivos."
        )

    return seccion



class MotorInterpretacionProfesional:
    """
    Motor de Interpretación Profesional de Claridata.

    Recibe los resultados del MotorEstadistico y del MotorDescubrimientos
    y genera interpretaciones escritas con lenguaje profesional, organizadas
    en secciones dinámicas.

    Principios:
    - Nunca recalcula estadísticas.
    - Nunca accede al dataset directamente.
    - Completamente determinístico y desacoplado.
    - La interfaz permanece estable para futura integración con LLM.
    """

    def interpretar(
        self,
        estadistico: ResultadoMotorEstadistico,
        descubrimientos: ResultadoMotorDescubrimientos,
    ) -> ResultadoMotorInterpretacion:
        resultado = ResultadoMotorInterpretacion()

        resultado.agregar_seccion(
            _generar_resumen_general(estadistico, descubrimientos)
        )
        resultado.agregar_seccion(
            _generar_variables_destacadas(estadistico)
        )
        resultado.agregar_seccion(
            _generar_patrones_detectados(estadistico, descubrimientos)
        )
        resultado.agregar_seccion(
            _generar_calidad_datos(estadistico, descubrimientos)
        )
        resultado.agregar_seccion(
            _generar_relaciones_encontradas(estadistico, descubrimientos)
        )
        resultado.agregar_seccion(
            _generar_implicaciones(estadistico, descubrimientos)
        )
        resultado.agregar_seccion(
            _generar_recomendaciones(estadistico, descubrimientos)
        )

        return resultado