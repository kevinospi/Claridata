from fastapi import Depends
from sqlalchemy.orm import Session

from infraestructura.base_de_datos.sesion import obtener_sesion_db
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from infraestructura.estadistica.motor_estadistico import MotorEstadistico
from infraestructura.ia.interfaz_interpretador import InterpretadorInforme
from infraestructura.ia.interfaz_interpretador_conversacional import (
    InterpretadorConversacional,
)
from infraestructura.ia.interpretador_reglas import InterpretadorReglas
from infraestructura.ia.interpretador_conversacional_reglas import (
    InterpretadorConversacionalReglas,
)


def obtener_repositorio_usuario(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioUsuario:
    return RepositorioUsuario(sesion)


def obtener_repositorio_dataset(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioDataset:
    return RepositorioDataset(sesion)


def obtener_repositorio_informe(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioInforme:
    return RepositorioInforme(sesion)


def obtener_repositorio_conversacion(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioConversacion:
    return RepositorioConversacion(sesion)


def obtener_repositorio_mensaje(
    sesion: Session = Depends(obtener_sesion_db),
) -> RepositorioMensaje:
    return RepositorioMensaje(sesion)


def obtener_motor_estadistico() -> MotorEstadistico:
    return MotorEstadistico()


def obtener_interpretador_informe() -> InterpretadorInforme:
    return InterpretadorReglas()


def obtener_interpretador_conversacional() -> InterpretadorConversacional:
    return InterpretadorConversacionalReglas()