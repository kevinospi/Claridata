from fastapi import Depends
from sqlalchemy.orm import Session

from infraestructura.base_de_datos.sesion import obtener_sesion_db
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset


def obtener_repositorio_usuario(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioUsuario:
    return RepositorioUsuario(sesion)


def obtener_repositorio_dataset(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioDataset:
    return RepositorioDataset(sesion)