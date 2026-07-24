import pandas as pd

from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.estadistica.dto_resultados import ResultadoMotorEstadistico
from infraestructura.estadistica.lector_dataset import FormatoArchivoNoSoportadoError
from infraestructura.estadistica.motor_estadistico import MotorEstadistico
from infraestructura.estadistica.motor_descubrimientos import MotorDescubrimientos
from infraestructura.estadistica.motor_interpretacion_profesional import MotorInterpretacionProfesional
from infraestructura.estadistica.motor_recomendaciones import MotorRecomendacionesInteligentes
from infraestructura.estadistica.motor_visualizaciones import MotorVisualizaciones
from aplicacion.excepciones import (
    AccesoDenegadoError,
    DatasetNoEncontradoError,
    ErrorAnalisisDataset,
)


class AnalizarDataset:
    def __init__(
        self,
        repositorio_dataset: RepositorioDataset,
        repositorio_informe: RepositorioInforme,
        motor_estadistico: MotorEstadistico,
        motor_descubrimientos: MotorDescubrimientos,
        motor_interpretacion: MotorInterpretacionProfesional,
        motor_recomendaciones: MotorRecomendacionesInteligentes,
        motor_visualizaciones: MotorVisualizaciones,
    ) -> None:
        self._repositorio_dataset = repositorio_dataset
        self._repositorio_informe = repositorio_informe
        self._motor_estadistico = motor_estadistico
        self._motor_descubrimientos = motor_descubrimientos
        self._motor_interpretacion = motor_interpretacion
        self._motor_recomendaciones = motor_recomendaciones
        self._motor_visualizaciones = motor_visualizaciones

    def ejecutar(self, dataset_id: str, usuario_id: str) -> InformeModelo:
        dataset = self._repositorio_dataset.obtener_por_id(dataset_id)
        if dataset is None:
            raise DatasetNoEncontradoError(f"No existe un dataset con id '{dataset_id}'.")

        if dataset.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para analizar este dataset.")

        try:
            resultado_estadistico = self._motor_estadistico.analizar(
                ruta_archivo=dataset.ruta_archivo,
                tipo_archivo=dataset.tipo_archivo,
            )
        except (
            FormatoArchivoNoSoportadoError,
            OSError,
            ValueError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
            UnicodeDecodeError,
        ) as error:
            raise ErrorAnalisisDataset(
                f"No fue posible analizar el dataset '{dataset_id}': {error}"
            ) from error

        resultado_descubrimientos = self._motor_descubrimientos.analizar(resultado_estadistico)
        resultado_interpretacion = self._motor_interpretacion.interpretar(resultado_estadistico, resultado_descubrimientos)
        resultado_recomendaciones = self._motor_recomendaciones.recomendar(resultado_estadistico, resultado_descubrimientos, resultado_interpretacion)
        resultado_visualizaciones = self._motor_visualizaciones.generar(resultado_estadistico, resultado_descubrimientos, resultado_interpretacion, resultado_recomendaciones)

        self._actualizar_metadatos_dataset(dataset, resultado_estadistico)
        self._repositorio_dataset.actualizar(dataset)
        self._repositorio_dataset.guardar_cambios()

        descubrimientos_dict = resultado_descubrimientos.como_lista_dict()
        interpretacion_dict = resultado_interpretacion.como_lista_dict()
        recomendaciones_dict = resultado_recomendaciones.como_lista_dict()
        visualizaciones_dict = resultado_visualizaciones.como_lista_dict()

        informe_existente = self._repositorio_informe.obtener_por_dataset(dataset_id)

        if informe_existente is not None:
            self._actualizar_informe(informe_existente, resultado_estadistico, descubrimientos_dict, interpretacion_dict, recomendaciones_dict, visualizaciones_dict)
            self._repositorio_informe.actualizar(informe_existente)
            self._repositorio_informe.guardar_cambios()
            return informe_existente

        nuevo_informe = self._construir_informe(dataset, usuario_id, resultado_estadistico, descubrimientos_dict, interpretacion_dict, recomendaciones_dict, visualizaciones_dict)
        self._repositorio_informe.crear(nuevo_informe)
        self._repositorio_informe.guardar_cambios()
        return nuevo_informe

    def _actualizar_metadatos_dataset(self, dataset, resultado: ResultadoMotorEstadistico) -> None:
        dataset.numero_filas = resultado.metadatos.numero_filas
        dataset.numero_columnas = resultado.metadatos.numero_columnas
        dataset.columnas = resultado.metadatos.nombres_columnas
        dataset.tipos_datos = resultado.metadatos.tipos_datos

    def _construir_informe(self, dataset, usuario_id, resultado, descubrimientos, interpretacion, recomendaciones, visualizaciones) -> InformeModelo:
        informe = InformeModelo(usuario_id=usuario_id, dataset_id=dataset.id, titulo=dataset.nombre_archivo, guardado=False)
        self._actualizar_informe(informe, resultado, descubrimientos, interpretacion, recomendaciones, visualizaciones)
        return informe

    def _actualizar_informe(self, informe, resultado, descubrimientos, interpretacion, recomendaciones, visualizaciones) -> None:
        informe.estadisticas_descriptivas = self._mapear_estadisticas_descriptivas(resultado)
        informe.analisis_distribucion = self._mapear_distribuciones(resultado)
        informe.correlaciones = self._mapear_correlaciones(resultado)
        informe.deteccion_outliers = self._mapear_outliers(resultado)
        informe.descubrimientos = descubrimientos
        informe.interpretacion_profesional = interpretacion
        informe.recomendaciones_inteligentes = recomendaciones
        informe.visualizaciones_inteligentes = visualizaciones

    def _mapear_estadisticas_descriptivas(self, resultado: ResultadoMotorEstadistico) -> dict:
        return {
            "metadatos": {
                "numero_filas": resultado.metadatos.numero_filas,
                "numero_columnas": resultado.metadatos.numero_columnas,
                "nombres_columnas": resultado.metadatos.nombres_columnas,
                "tipos_datos": resultado.metadatos.tipos_datos,
            },
            "valores_nulos": {
                "por_columna": resultado.valores_nulos.por_columna,
                "total": resultado.valores_nulos.total,
            },
            "clasificacion_variables": {
                "numericas": resultado.clasificacion_variables.numericas,
                "categoricas": resultado.clasificacion_variables.categoricas,
            },
            "columnas": [
                {
                    "columna": est.columna,
                    "media": est.media,
                    "mediana": est.mediana,
                    "desviacion_estandar": est.desviacion_estandar,
                    "minimo": est.minimo,
                    "maximo": est.maximo,
                }
                for est in resultado.estadisticas_descriptivas
            ],
        }

    def _mapear_distribuciones(self, resultado: ResultadoMotorEstadistico) -> dict:
        return {"columnas": [{"columna": d.columna, "asimetria": d.asimetria, "curtosis": d.curtosis} for d in resultado.distribuciones]}

    def _mapear_correlaciones(self, resultado: ResultadoMotorEstadistico) -> dict | None:
        if resultado.correlaciones is None:
            return None
        return {
            "matriz": resultado.correlaciones.matriz,
            "umbral_relevancia": resultado.correlaciones.umbral_relevancia,
            "pares_relevantes": [{"columna_a": p.columna_a, "columna_b": p.columna_b, "coeficiente": p.coeficiente} for p in resultado.correlaciones.pares_relevantes],
        }

    def _mapear_outliers(self, resultado: ResultadoMotorEstadistico) -> dict:
        return {"columnas": [{"columna": o.columna, "q1": o.q1, "q3": o.q3, "iqr": o.iqr, "limite_inferior": o.limite_inferior, "limite_superior": o.limite_superior, "cantidad_outliers": o.cantidad_outliers} for o in resultado.outliers]}