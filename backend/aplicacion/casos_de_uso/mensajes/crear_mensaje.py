from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from aplicacion.excepciones import AccesoDenegadoError, ConversacionNoEncontradaError


class CrearMensaje:
    def __init__(
        self,
        repositorio_mensaje: RepositorioMensaje,
        repositorio_conversacion: RepositorioConversacion,
    ) -> None:
        self._repositorio_mensaje = repositorio_mensaje
        self._repositorio_conversacion = repositorio_conversacion

    def ejecutar(
        self,
        conversacion_id: str,
        usuario_id: str,
        rol: str,
        contenido: str,
        tipo_respuesta: str | None = None,
    ) -> MensajeModelo:
        conversacion = self._repositorio_conversacion.obtener_por_id(conversacion_id)
        if conversacion is None:
            raise ConversacionNoEncontradaError(
                f"No existe una conversación con id '{conversacion_id}'."
            )

        if conversacion.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para escribir en esta conversación.")

        nuevo_mensaje = MensajeModelo(
            conversacion_id=conversacion_id,
            rol=rol,
            contenido=contenido,
            tipo_respuesta=tipo_respuesta,
        )

        self._repositorio_mensaje.crear(nuevo_mensaje)
        self._repositorio_mensaje.guardar_cambios()
        return nuevo_mensaje