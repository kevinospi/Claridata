from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.ia.dto_conversacion import ContextoInforme, MensajeContexto


class ConstructorContextoInforme:
    def construir(
        self,
        informe: InformeModelo,
        historial_mensajes: list[MensajeModelo],
    ) -> ContextoInforme:
        historial = [
            MensajeContexto(rol=mensaje.rol, contenido=mensaje.contenido)
            for mensaje in historial_mensajes
        ]

        return ContextoInforme(
            resumen_ejecutivo=informe.resumen_ejecutivo,
            conclusiones=informe.conclusiones,
            hallazgos_principales=informe.hallazgos_principales,
            recomendaciones=informe.recomendaciones,
            correlaciones=informe.correlaciones,
            deteccion_outliers=informe.deteccion_outliers,
            analisis_distribucion=informe.analisis_distribucion,
            historial=historial,
        )