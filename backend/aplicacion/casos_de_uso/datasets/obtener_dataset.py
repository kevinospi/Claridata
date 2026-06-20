from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from aplicacion.excepciones import DatasetNoEncontradoError


class ObtenerDataset:
    def __init__(self, repositorio_dataset: RepositorioDataset) -> None:
        self._repositorio_dataset = repositorio_dataset

    def ejecutar(self, dataset_id: str) -> DatasetModelo:
        dataset = self._repositorio_dataset.obtener_por_id(dataset_id)
        if dataset is None:
            raise DatasetNoEncontradoError(f"No existe un dataset con id '{dataset_id}'.")
        return dataset