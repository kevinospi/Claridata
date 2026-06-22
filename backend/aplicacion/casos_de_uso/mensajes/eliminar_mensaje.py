from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from aplicacion.excepciones import MensajeNoEncontradoError


class EliminarMensaje:
    def __init__(self, repositorio_mensaje: RepositorioMensaje) -> None:
        self._repositorio_mensaje = repositorio_mensaje

    def ejecutar(self, mensaje_id: str) -> None:
        mensaje = self._repositorio_mensaje.obtener_por_id(mensaje_id)
        if mensaje is None:
            raise MensajeNoEncontradoError(f"No existe un mensaje con id '{mensaje_id}'.")

        self._repositorio_mensaje.eliminar(mensaje)
        self._repositorio_mensaje.guardar_cambios()