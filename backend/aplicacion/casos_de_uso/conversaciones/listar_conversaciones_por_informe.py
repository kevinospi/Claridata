from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from aplicacion.excepciones import AccesoDenegadoError, InformeNoEncontradoError


class ListarConversacionesPorInforme:
    def __init__(
        self,
        repositorio_conversacion: RepositorioConversacion,
        repositorio_informe: RepositorioInforme,
    ) -> None:
        self._repositorio_conversacion = repositorio_conversacion
        self._repositorio_informe = repositorio_informe

    def ejecutar(self, informe_id: str, usuario_id: str) -> list[ConversacionModelo]:
        informe = self._repositorio_informe.obtener_por_id(informe_id)
        if informe is None:
            raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

        if informe.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para acceder a este informe.")

        return self._repositorio_conversacion.obtener_por_informe(informe_id)