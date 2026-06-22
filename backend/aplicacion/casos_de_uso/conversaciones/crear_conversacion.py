from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from aplicacion.excepciones import (
    AccesoDenegadoError,
    InformeNoEncontradoError,
    TipoConversacionInvalidoError,
)

_TIPOS_VALIDOS = {"informe", "aprendizaje"}


class CrearConversacion:
    def __init__(
        self,
        repositorio_conversacion: RepositorioConversacion,
        repositorio_informe: RepositorioInforme,
    ) -> None:
        self._repositorio_conversacion = repositorio_conversacion
        self._repositorio_informe = repositorio_informe

    def ejecutar(
        self,
        usuario_id: str,
        tipo_conversacion: str,
        informe_id: str | None = None,
    ) -> ConversacionModelo:
        if tipo_conversacion not in _TIPOS_VALIDOS:
            raise TipoConversacionInvalidoError(
                f"tipo_conversacion debe ser uno de {_TIPOS_VALIDOS}, recibido: '{tipo_conversacion}'."
            )

        if tipo_conversacion == "informe" and informe_id is None:
            raise TipoConversacionInvalidoError(
                "Una conversación de tipo 'informe' requiere informe_id."
            )

        if tipo_conversacion == "aprendizaje" and informe_id is not None:
            raise TipoConversacionInvalidoError(
                "Una conversación de tipo 'aprendizaje' no debe tener informe_id."
            )

        if tipo_conversacion == "informe":
            informe = self._repositorio_informe.obtener_por_id(informe_id)
            if informe is None:
                raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

            if informe.usuario_id != usuario_id:
                raise AccesoDenegadoError(
                    "No tienes permiso para crear una conversación sobre este informe."
                )

        nueva_conversacion = ConversacionModelo(
            usuario_id=usuario_id,
            informe_id=informe_id,
            tipo_conversacion=tipo_conversacion,
        )

        self._repositorio_conversacion.crear(nueva_conversacion)
        self._repositorio_conversacion.guardar_cambios()
        return nueva_conversacion