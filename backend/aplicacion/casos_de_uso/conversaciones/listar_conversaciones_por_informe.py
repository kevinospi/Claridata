from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)


class ListarConversacionesPorInforme:
    def __init__(self, repositorio_conversacion: RepositorioConversacion) -> None:
        self._repositorio_conversacion = repositorio_conversacion

    def ejecutar(self, informe_id: str) -> list[ConversacionModelo]:
        return self._repositorio_conversacion.obtener_por_informe(informe_id)