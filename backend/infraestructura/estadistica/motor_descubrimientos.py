from infraestructura.estadistica.dto_descubrimientos import (
    Descubrimiento,
    ResultadoMotorDescubrimientos,
    SeveridadDescubrimiento,
    TipoDescubrimiento,
)
from infraestructura.estadistica.dto_resultados import ResultadoMotorEstadistico

# ─── Umbrales configurables ────────────────────────────────────────────────────

_UMBRAL_OUTLIERS_POCOS = 0.05      # < 5 % de filas
_UMBRAL_OUTLIERS_MUCHOS = 0.15     # ≥ 15 % de filas
_UMBRAL_ASIMETRIA_SIMETRICA = 0.5  # |asimetría| < 0.5  → simétrica
_UMBRAL_ASIMETRIA_FUERTE = 1.0     # |asimetría| ≥ 1.0  → fuerte
_UMBRAL_CURTOSIS_NORMAL = 1.0      # |curtosis|  < 1.0  → normal
_UMBRAL_CURTOSIS_PESADA = 3.0      # curtosis    ≥ 3.0  → colas pesadas
_UMBRAL_CORRELACION_FUERTE = 0.8   # |r| ≥ 0.8
_UMBRAL_FALTANTES_PARCIAL = 0.05   # 5–30 % faltantes → parcial
_UMBRAL_FALTANTES_CRITICO = 0.30   # ≥ 30 % faltantes → crítico
_UMBRAL_CV_ALTA = 1.0              # CV ≥ 100 % → alta variabilidad
_UMBRAL_CV_BAJA = 0.05             # CV ≤  5 % → baja variabilidad
_UMBRAL_CEROS_SOSPECHOSO = 0.50    # ≥ 50 % ceros → sospechoso
_UMBRAL_REPETIDOS_SOSPECHOSO = 0.80 # ≥ 80 % mismo valor → sospechoso


# ─── Reglas independientes ────────────────────────────────────────────────────

def _detectar_outliers(
    resultado: ResultadoMotorEstadistico,
    total_filas: int,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []

    for outlier in resultado.outliers:
        if total_filas == 0:
            continue

        proporcion = outlier.cantidad_outliers / total_filas

        if outlier.cantidad_outliers == 0:
            continue

        if proporcion < _UMBRAL_OUTLIERS_POCOS:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.OUTLIERS,
                    titulo=f"Pocos valores atípicos en '{outlier.columna}'",
                    descripcion=(
                        f"La variable '{outlier.columna}' presenta "
                        f"{outlier.cantidad_outliers} valor(es) atípico(s) "
                        f"({proporcion * 100:.1f}% de los datos). "
                        "Su impacto sobre la media es probablemente bajo."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=outlier.columna,
                    valor=float(outlier.cantidad_outliers),
                    recomendacion=(
                        "Revisar estos valores para confirmar que no son errores de captura."
                    ),
                )
            )
        elif proporcion >= _UMBRAL_OUTLIERS_MUCHOS:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.OUTLIERS,
                    titulo=f"Muchos valores atípicos en '{outlier.columna}'",
                    descripcion=(
                        f"La variable '{outlier.columna}' presenta "
                        f"{outlier.cantidad_outliers} valores atípicos "
                        f"({proporcion * 100:.1f}% de los datos), lo que podría "
                        "influir considerablemente sobre medidas como la media."
                    ),
                    severidad=SeveridadDescubrimiento.IMPORTANTE,
                    columna=outlier.columna,
                    valor=float(outlier.cantidad_outliers),
                    recomendacion=(
                        "Evaluar si estos valores son errores o fenómenos reales "
                        "antes de entrenar modelos o calcular estadísticas agregadas."
                    ),
                )
            )
        else:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.OUTLIERS,
                    titulo=f"Valores atípicos detectados en '{outlier.columna}'",
                    descripcion=(
                        f"La variable '{outlier.columna}' presenta "
                        f"{outlier.cantidad_outliers} valores atípicos "
                        f"({proporcion * 100:.1f}% de los datos)."
                    ),
                    severidad=SeveridadDescubrimiento.ATENCION,
                    columna=outlier.columna,
                    valor=float(outlier.cantidad_outliers),
                    recomendacion=(
                        "Investigar el origen de estos valores antes de continuar el análisis."
                    ),
                )
            )

    return descubrimientos


def _detectar_asimetria(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []

    for dist in resultado.distribuciones:
        asimetria = dist.asimetria
        abs_asimetria = abs(asimetria)

        if abs_asimetria < _UMBRAL_ASIMETRIA_SIMETRICA:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.ASIMETRIA,
                    titulo=f"Distribución aproximadamente simétrica en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' presenta una distribución "
                        f"aproximadamente simétrica (asimetría = {asimetria:.2f}). "
                        "La media y la mediana deberían ser similares."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=dist.columna,
                    valor=round(asimetria, 4),
                    recomendacion=None,
                )
            )
        elif abs_asimetria >= _UMBRAL_ASIMETRIA_FUERTE:
            direccion = "positiva" if asimetria > 0 else "negativa"
            descripcion_dir = (
                "con una cola hacia valores altos"
                if asimetria > 0
                else "con una cola hacia valores bajos"
            )
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.ASIMETRIA,
                    titulo=f"Asimetría {direccion} fuerte en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' presenta una asimetría "
                        f"{direccion} fuerte (asimetría = {asimetria:.2f}), "
                        f"{descripcion_dir}. La media estará alejada de la mediana."
                    ),
                    severidad=SeveridadDescubrimiento.ATENCION,
                    columna=dist.columna,
                    valor=round(asimetria, 4),
                    recomendacion=(
                        "Considerar usar la mediana como medida de tendencia central "
                        "y evaluar una transformación logarítmica si se va a modelar."
                    ),
                )
            )
        else:
            direccion = "positiva" if asimetria > 0 else "negativa"
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.ASIMETRIA,
                    titulo=f"Ligera asimetría {direccion} en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' presenta una ligera asimetría "
                        f"{direccion} (asimetría = {asimetria:.2f})."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=dist.columna,
                    valor=round(asimetria, 4),
                    recomendacion=None,
                )
            )

    return descubrimientos


def _detectar_curtosis(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []

    for dist in resultado.distribuciones:
        curtosis = dist.curtosis

        if abs(curtosis) < _UMBRAL_CURTOSIS_NORMAL:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.CURTOSIS,
                    titulo=f"Curtosis normal en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' tiene una curtosis de "
                        f"{curtosis:.2f}, compatible con una distribución normal."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=dist.columna,
                    valor=round(curtosis, 4),
                    recomendacion=None,
                )
            )
        elif curtosis >= _UMBRAL_CURTOSIS_PESADA:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.CURTOSIS,
                    titulo=f"Colas pesadas detectadas en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' tiene una curtosis alta "
                        f"({curtosis:.2f}), lo que indica colas pesadas y mayor "
                        "probabilidad de valores extremos de lo esperado en una distribución normal."
                    ),
                    severidad=SeveridadDescubrimiento.ATENCION,
                    columna=dist.columna,
                    valor=round(curtosis, 4),
                    recomendacion=(
                        "Prestar especial atención a los valores extremos. "
                        "Modelos que asumen normalidad podrían no ser apropiados."
                    ),
                )
            )
        elif curtosis <= -_UMBRAL_CURTOSIS_NORMAL:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.CURTOSIS,
                    titulo=f"Colas ligeras en '{dist.columna}'",
                    descripcion=(
                        f"La variable '{dist.columna}' tiene una curtosis baja "
                        f"({curtosis:.2f}), indicando colas más ligeras que una "
                        "distribución normal y concentración de valores en el centro."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=dist.columna,
                    valor=round(curtosis, 4),
                    recomendacion=None,
                )
            )

    return descubrimientos


def _detectar_correlaciones(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    if resultado.correlaciones is None:
        return []

    descubrimientos: list[Descubrimiento] = []

    for par in resultado.correlaciones.pares_relevantes:
        coef = par.coeficiente

        if coef >= _UMBRAL_CORRELACION_FUERTE:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.CORRELACION_FUERTE,
                    titulo=f"Correlación positiva muy alta: '{par.columna_a}' y '{par.columna_b}'",
                    descripcion=(
                        f"Se detectó una correlación positiva muy alta (r = {coef:.2f}) "
                        f"entre '{par.columna_a}' y '{par.columna_b}'. "
                        "A medida que una variable aumenta, la otra tiende a aumentar también."
                    ),
                    severidad=SeveridadDescubrimiento.IMPORTANTE,
                    columna=f"{par.columna_a} / {par.columna_b}",
                    valor=round(coef, 4),
                    recomendacion=(
                        "Verificar si existe una relación causal o si ambas variables "
                        "miden el mismo fenómeno. Considerar eliminar una si se va a modelar."
                    ),
                )
            )
        elif coef <= -_UMBRAL_CORRELACION_FUERTE:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.CORRELACION_NEGATIVA,
                    titulo=f"Correlación negativa muy alta: '{par.columna_a}' y '{par.columna_b}'",
                    descripcion=(
                        f"Se detectó una correlación negativa muy alta (r = {coef:.2f}) "
                        f"entre '{par.columna_a}' y '{par.columna_b}'. "
                        "A medida que una variable aumenta, la otra tiende a disminuir."
                    ),
                    severidad=SeveridadDescubrimiento.IMPORTANTE,
                    columna=f"{par.columna_a} / {par.columna_b}",
                    valor=round(coef, 4),
                    recomendacion=(
                        "Investigar la naturaleza de esta relación inversa "
                        "antes de incluir ambas variables en un modelo predictivo."
                    ),
                )
            )

    return descubrimientos


def _detectar_valores_faltantes(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []
    total_filas = resultado.metadatos.numero_filas

    if total_filas == 0:
        return descubrimientos

    for columna, cantidad in resultado.valores_nulos.por_columna.items():
        if cantidad == 0:
            continue

        proporcion = cantidad / total_filas

        if proporcion >= _UMBRAL_FALTANTES_CRITICO:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.VALORES_FALTANTES,
                    titulo=f"Alta cantidad de faltantes en '{columna}'",
                    descripcion=(
                        f"La variable '{columna}' tiene {cantidad} valores faltantes "
                        f"({proporcion * 100:.1f}% de los registros). "
                        "Una proporción tan alta puede comprometer la calidad del análisis."
                    ),
                    severidad=SeveridadDescubrimiento.CRITICO,
                    columna=columna,
                    valor=round(proporcion * 100, 2),
                    recomendacion=(
                        "Evaluar si esta columna debe incluirse en el análisis. "
                        "Considerar imputación o eliminación según el contexto."
                    ),
                )
            )
        else:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.VALORES_FALTANTES,
                    titulo=f"Valores faltantes en '{columna}'",
                    descripcion=(
                        f"La variable '{columna}' tiene {cantidad} valores faltantes "
                        f"({proporcion * 100:.1f}% de los registros)."
                    ),
                    severidad=SeveridadDescubrimiento.ATENCION,
                    columna=columna,
                    valor=round(proporcion * 100, 2),
                    recomendacion=(
                        "Revisar el origen de los datos faltantes y "
                        "considerar imputación si es necesario."
                    ),
                )
            )

    return descubrimientos


def _detectar_variables_constantes(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []

    for est in resultado.estadisticas_descriptivas:
        if est.maximo == est.minimo:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.VARIABLE_CONSTANTE,
                    titulo=f"Variable constante: '{est.columna}'",
                    descripcion=(
                        f"La variable '{est.columna}' tiene el mismo valor "
                        f"({est.minimo}) en todos los registros. "
                        "No aporta información para el análisis."
                    ),
                    severidad=SeveridadDescubrimiento.IMPORTANTE,
                    columna=est.columna,
                    valor=est.minimo,
                    recomendacion=(
                        "Considerar eliminar esta columna ya que no contiene variabilidad útil."
                    ),
                )
            )

    return descubrimientos


def _detectar_variabilidad(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []

    for est in resultado.estadisticas_descriptivas:
        if est.media == 0:
            continue

        cv = abs(est.desviacion_estandar / est.media)

        if cv >= _UMBRAL_CV_ALTA:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.ALTA_VARIABILIDAD,
                    titulo=f"Alta variabilidad en '{est.columna}'",
                    descripcion=(
                        f"La variable '{est.columna}' presenta una variabilidad muy alta "
                        f"(coeficiente de variación = {cv * 100:.1f}%). "
                        "Los datos están muy dispersos respecto a la media."
                    ),
                    severidad=SeveridadDescubrimiento.ATENCION,
                    columna=est.columna,
                    valor=round(cv * 100, 2),
                    recomendacion=(
                        "Investigar el origen de esta dispersión. "
                        "Puede indicar subgrupos distintos o valores atípicos relevantes."
                    ),
                )
            )
        elif cv <= _UMBRAL_CV_BAJA and est.maximo != est.minimo:
            descubrimientos.append(
                Descubrimiento(
                    tipo=TipoDescubrimiento.BAJA_VARIABILIDAD,
                    titulo=f"Baja variabilidad en '{est.columna}'",
                    descripcion=(
                        f"La variable '{est.columna}' presenta muy poca variabilidad "
                        f"(coeficiente de variación = {cv * 100:.1f}%). "
                        "Los valores son casi constantes."
                    ),
                    severidad=SeveridadDescubrimiento.INFORMATIVO,
                    columna=est.columna,
                    valor=round(cv * 100, 2),
                    recomendacion=(
                        "Verificar si esta baja variabilidad es esperada en el contexto del análisis."
                    ),
                )
            )

    return descubrimientos


def _detectar_distribuciones_sospechosas(
    resultado: ResultadoMotorEstadistico,
) -> list[Descubrimiento]:
    descubrimientos: list[Descubrimiento] = []
    total_filas = resultado.metadatos.numero_filas

    if total_filas == 0:
        return descubrimientos

    for est in resultado.estadisticas_descriptivas:
        if est.minimo == 0:
            proporcion_ceros = (total_filas - est.media * total_filas / max(est.media, 0.001))
            pass

    tipos_datos = resultado.metadatos.tipos_datos
    for columna, tipo in tipos_datos.items():
        if "int" in tipo.lower() or "float" in tipo.lower():
            est_col = next(
                (e for e in resultado.estadisticas_descriptivas if e.columna == columna),
                None,
            )
            if est_col is None:
                continue

            rango = est_col.maximo - est_col.minimo
            if (
                rango > 0
                and est_col.minimo >= 0
                and est_col.maximo <= 20
                and "int" in tipo.lower()
            ):
                descubrimientos.append(
                    Descubrimiento(
                        tipo=TipoDescubrimiento.DISTRIBUCION_SOSPECHOSA,
                        titulo=f"Posible variable categórica en '{columna}'",
                        descripcion=(
                            f"La variable '{columna}' es numérica entera con un rango pequeño "
                            f"(de {est_col.minimo:.0f} a {est_col.maximo:.0f}). "
                            "Podría representar una categoría codificada numéricamente."
                        ),
                        severidad=SeveridadDescubrimiento.INFORMATIVO,
                        columna=columna,
                        valor=rango,
                        recomendacion=(
                            "Verificar si esta columna representa categorías "
                            "(ej. 1=Sí, 0=No) y tratarla adecuadamente en el análisis."
                        ),
                    )
                )

    return descubrimientos


# ─── Orquestador ──────────────────────────────────────────────────────────────

class MotorDescubrimientos:
    """
    Orquestador del Motor de Descubrimientos.
    Nunca recalcula estadísticas — trabaja exclusivamente sobre
    ResultadoMotorEstadistico ya calculado por MotorEstadistico.
    """

    def analizar(
        self, resultado: ResultadoMotorEstadistico
    ) -> ResultadoMotorDescubrimientos:
        resultado_final = ResultadoMotorDescubrimientos()

        total_filas = resultado.metadatos.numero_filas

        for descubrimiento in _detectar_outliers(resultado, total_filas):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_asimetria(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_curtosis(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_correlaciones(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_valores_faltantes(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_variables_constantes(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_variabilidad(resultado):
            resultado_final.agregar(descubrimiento)

        for descubrimiento in _detectar_distribuciones_sospechosas(resultado):
            resultado_final.agregar(descubrimiento)

        return resultado_final