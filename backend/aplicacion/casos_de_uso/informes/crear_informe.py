from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme


class CrearInforme:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(
        self,
        usuario_id: str,
        dataset_id: str,
        resumen_ejecutivo: str | None = None,
        estadisticas_descriptivas: dict | None = None,
        analisis_distribucion: dict | None = None,
        correlaciones: dict | None = None,
        deteccion_outliers: dict | None = None,
        hallazgos_principales: dict | None = None,
        recomendaciones: dict | None = None,
        conclusiones: str | None = None,
    ) -> InformeModelo:
        nuevo_informe = InformeModelo(
            usuario_id=usuario_id,
            dataset_id=dataset_id,
            guardado=False,
            resumen_ejecutivo=resumen_ejecutivo,
            estadisticas_descriptivas=estadisticas_descriptivas,
            analisis_distribucion=analisis_distribucion,
            correlaciones=correlaciones,
            deteccion_outliers=deteccion_outliers,
            hallazgos_principales=hallazgos_principales,
            recomendaciones=recomendaciones,
            conclusiones=conclusiones,
        )

        self._repositorio_informe.crear(nuevo_informe)
        self._repositorio_informe.guardar_cambios()
        return nuevo_informe