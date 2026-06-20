from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje


class CrearMensaje:
    def __init__(self, repositorio_mensaje: RepositorioMensaje) -> None:
        self._repositorio_mensaje = repositorio_mensaje

    def ejecutar(
        self,
        conversacion_id: str,
        rol: str,
        contenido: str,
        tipo_respuesta: str | None = None,
    ) -> MensajeModelo:
        nuevo_mensaje = MensajeModelo(
            conversacion_id=conversacion_id,
            rol=rol,
            contenido=contenido,
            tipo_respuesta=tipo_respuesta,
        )

        self._repositorio_mensaje.crear(nuevo_mensaje)
        self._repositorio_mensaje.guardar_cambios()
        return nuevo_mensaje