from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from aplicacion.excepciones import InformeNoEncontradoError


class EliminarInforme:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(self, informe_id: str) -> None:
        informe = self._repositorio_informe.obtener_por_id(informe_id)
        if informe is None:
            raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

        self._repositorio_informe.eliminar(informe)
        self._repositorio_informe.guardar_cambios()