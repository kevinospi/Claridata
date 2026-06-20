from fastapi import APIRouter, Depends, UploadFile

from aplicacion.casos_de_uso.datasets.crear_dataset import CrearDataset
from aplicacion.casos_de_uso.datasets.obtener_dataset import ObtenerDataset
from aplicacion.casos_de_uso.datasets.listar_datasets_usuario import ListarDatasetsUsuario
from aplicacion.casos_de_uso.datasets.eliminar_dataset import EliminarDataset
from aplicacion.validadores.validador_dataset import ValidadorDataset
from infraestructura.almacenamiento.gestor_archivos import GestorArchivos
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_dataset
from presentacion.api.dependencias.dependencias_usuario import obtener_usuario_actual_id
from presentacion.esquemas.datasets.dataset_esquema import DatasetRespuestaEsquema

router = APIRouter()


@router.post(
    "/datasets",
    response_model=DatasetRespuestaEsquema,
    status_code=201,
    tags=["Datasets"],
)
async def crear_dataset(
    archivo: UploadFile,
    repositorio_dataset: RepositorioDataset = Depends(obtener_repositorio_dataset),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> DatasetRespuestaEsquema:
    contenido = await archivo.read()

    gestor_archivos = GestorArchivos()
    ruta_archivo = gestor_archivos.guardar(archivo.filename, contenido)

    tipo_archivo = archivo.filename.rsplit(".", maxsplit=1)[-1].lower()

    caso_de_uso = CrearDataset(repositorio_dataset, ValidadorDataset())
    dataset = caso_de_uso.ejecutar(
        usuario_id=usuario_id,
        nombre_archivo=archivo.filename,
        tipo_archivo=tipo_archivo,
        ruta_archivo=ruta_archivo,
        tamaño_archivo=len(contenido),
    )
    return DatasetRespuestaEsquema.model_validate(dataset)


@router.get(
    "/datasets",
    response_model=list[DatasetRespuestaEsquema],
    tags=["Datasets"],
)
def listar_datasets(
    repositorio_dataset: RepositorioDataset = Depends(obtener_repositorio_dataset),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> list[DatasetRespuestaEsquema]:
    caso_de_uso = ListarDatasetsUsuario(repositorio_dataset)
    datasets = caso_de_uso.ejecutar(usuario_id)
    return [DatasetRespuestaEsquema.model_validate(d) for d in datasets]


@router.get(
    "/datasets/{dataset_id}",
    response_model=DatasetRespuestaEsquema,
    tags=["Datasets"],
)
def obtener_dataset(
    dataset_id: str,
    repositorio_dataset: RepositorioDataset = Depends(obtener_repositorio_dataset),
) -> DatasetRespuestaEsquema:
    caso_de_uso = ObtenerDataset(repositorio_dataset)
    dataset = caso_de_uso.ejecutar(dataset_id)
    return DatasetRespuestaEsquema.model_validate(dataset)


@router.delete(
    "/datasets/{dataset_id}",
    status_code=204,
    tags=["Datasets"],
)
def eliminar_dataset(
    dataset_id: str,
    repositorio_dataset: RepositorioDataset = Depends(obtener_repositorio_dataset),
) -> None:
    caso_de_uso = EliminarDataset(repositorio_dataset)
    caso_de_uso.ejecutar(dataset_id)