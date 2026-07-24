from sqlalchemy.orm import Session
from fastapi import Depends

from infraestructura.base_de_datos.sesion import SessionLocal
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import RepositorioConversacion
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from infraestructura.estadistica.motor_estadistico import MotorEstadistico
from infraestructura.estadistica.motor_descubrimientos import MotorDescubrimientos
from infraestructura.ia.interfaz_interpretador import InterpretadorInforme
from infraestructura.ia.interpretador_reglas import InterpretadorReglas
from infraestructura.ia.interfaz_interpretador_conversacional import InterpretadorConversacional
from infraestructura.ia.interpretador_conversacional_reglas import InterpretadorConversacionalReglas
from infraestructura.estadistica.motor_interpretacion_profesional import MotorInterpretacionProfesional
from infraestructura.estadistica.motor_recomendaciones import MotorRecomendacionesInteligentes
from infraestructura.estadistica.motor_visualizaciones import MotorVisualizaciones


def obtener_sesion_db():
    sesion = SessionLocal()
    try:
        yield sesion
    except Exception:
        sesion.rollback()
        raise
    finally:
        sesion.close()


def obtener_repositorio_usuario(sesion: Session = Depends(obtener_sesion_db)):
    return RepositorioUsuario(sesion)


def obtener_repositorio_dataset(sesion: Session = Depends(obtener_sesion_db)):
    return RepositorioDataset(sesion)


def obtener_repositorio_informe(sesion: Session = Depends(obtener_sesion_db)):
    return RepositorioInforme(sesion)


def obtener_repositorio_conversacion(sesion: Session = Depends(obtener_sesion_db)):
    return RepositorioConversacion(sesion)


def obtener_repositorio_mensaje(sesion: Session = Depends(obtener_sesion_db)):
    return RepositorioMensaje(sesion)


def obtener_motor_estadistico() -> MotorEstadistico:
    return MotorEstadistico()


def obtener_motor_descubrimientos() -> MotorDescubrimientos:
    return MotorDescubrimientos()


def obtener_interpretador_informe() -> InterpretadorInforme:
    return InterpretadorReglas()


def obtener_interpretador_conversacional() -> InterpretadorConversacional:
    return InterpretadorConversacionalReglas()


def obtener_motor_interpretacion() -> MotorInterpretacionProfesional:
    return MotorInterpretacionProfesional()


def obtener_motor_recomendaciones() -> MotorRecomendacionesInteligentes:
    return MotorRecomendacionesInteligentes()


def obtener_motor_visualizaciones() -> MotorVisualizaciones:
    return MotorVisualizaciones()