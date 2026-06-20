from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje


class ListarMensajesConversacion:
    def __init__(self, repositorio_mensaje: RepositorioMensaje) -> None:
        self._repositorio_mensaje = repositorio_mensaje

    def ejecutar(self, conversacion_id: str) -> list[MensajeModelo]:
        return self._repositorio_mensaje.obtener_por_conversacion(conversacion_id)