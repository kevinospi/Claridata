from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from aplicacion.excepciones import ConversacionNoEncontradaError


class ObtenerConversacion:
    def __init__(self, repositorio_conversacion: RepositorioConversacion) -> None:
        self._repositorio_conversacion = repositorio_conversacion

    def ejecutar(self, conversacion_id: str) -> ConversacionModelo:
        conversacion = self._repositorio_conversacion.obtener_por_id(conversacion_id)
        if conversacion is None:
            raise ConversacionNoEncontradaError(
                f"No existe una conversación con id '{conversacion_id}'."
            )
        return conversacion