import os

from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from aplicacion.excepciones import AccesoDenegadoError, DatasetNoEncontradoError


class EliminarDataset:
    def __init__(self, repositorio_dataset: RepositorioDataset) -> None:
        self._repositorio_dataset = repositorio_dataset

    def ejecutar(self, dataset_id: str, usuario_id: str) -> None:
        dataset = self._repositorio_dataset.obtener_por_id(dataset_id)
        if dataset is None:
            raise DatasetNoEncontradoError(f"No existe un dataset con id '{dataset_id}'.")

        if dataset.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para eliminar este dataset.")

        ruta_archivo = dataset.ruta_archivo

        self._repositorio_dataset.eliminar(dataset)
        self._repositorio_dataset.guardar_cambios()

        self._eliminar_archivo_fisico(ruta_archivo)

    def _eliminar_archivo_fisico(self, ruta_archivo: str) -> None:
        try:
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        except OSError:
            pass