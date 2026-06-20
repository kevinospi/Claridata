from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset


class ListarDatasetsUsuario:
    def __init__(self, repositorio_dataset: RepositorioDataset) -> None:
        self._repositorio_dataset = repositorio_dataset

    def ejecutar(self, usuario_id: str) -> list[DatasetModelo]:
        return self._repositorio_dataset.obtener_por_usuario(usuario_id)