from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.informes.crear_informe import CrearInforme
from aplicacion.casos_de_uso.informes.obtener_informe import ObtenerInforme
from aplicacion.casos_de_uso.informes.guardar_informe import GuardarInforme
from aplicacion.casos_de_uso.informes.eliminar_informe import EliminarInforme
from aplicacion.casos_de_uso.informes.listar_informes_guardados import ListarInformesGuardados
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_informe
from presentacion.api.dependencias.dependencias_usuario import obtener_usuario_actual_id
from presentacion.esquemas.informes.informe_esquema import (
    InformeCreacionEsquema,
    InformeRespuestaEsquema,
)

router = APIRouter()


@router.post(
    "/informes",
    response_model=InformeRespuestaEsquema,
    status_code=201,
    tags=["Informes"],
)
def crear_informe(
    datos: InformeCreacionEsquema,
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> InformeRespuestaEsquema:
    caso_de_uso = CrearInforme(repositorio_informe)
    informe = caso_de_uso.ejecutar(
        usuario_id=usuario_id,
        dataset_id=datos.dataset_id,
        resumen_ejecutivo=datos.resumen_ejecutivo,
        estadisticas_descriptivas=datos.estadisticas_descriptivas,
        analisis_distribucion=datos.analisis_distribucion,
        correlaciones=datos.correlaciones,
        deteccion_outliers=datos.deteccion_outliers,
        hallazgos_principales=datos.hallazgos_principales,
        recomendaciones=datos.recomendaciones,
        conclusiones=datos.conclusiones,
    )
    return InformeRespuestaEsquema.model_validate(informe)


@router.get(
    "/informes/guardados",
    response_model=list[InformeRespuestaEsquema],
    tags=["Informes"],
)
def listar_informes_guardados(
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
    usuario_id: str = Depends(obtener_usuario_actual_id),
) -> list[InformeRespuestaEsquema]:
    caso_de_uso = ListarInformesGuardados(repositorio_informe)
    informes = caso_de_uso.ejecutar(usuario_id)
    return [InformeRespuestaEsquema.model_validate(i) for i in informes]


@router.get(
    "/informes/{informe_id}",
    response_model=InformeRespuestaEsquema,
    tags=["Informes"],
)
def obtener_informe(
    informe_id: str,
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
) -> InformeRespuestaEsquema:
    caso_de_uso = ObtenerInforme(repositorio_informe)
    informe = caso_de_uso.ejecutar(informe_id)
    return InformeRespuestaEsquema.model_validate(informe)


@router.post(
    "/informes/{informe_id}/guardar",
    response_model=InformeRespuestaEsquema,
    tags=["Informes"],
)
def guardar_informe(
    informe_id: str,
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
) -> InformeRespuestaEsquema:
    caso_de_uso = GuardarInforme(repositorio_informe)
    informe = caso_de_uso.ejecutar(informe_id)
    return InformeRespuestaEsquema.model_validate(informe)


@router.delete(
    "/informes/{informe_id}",
    status_code=204,
    tags=["Informes"],
)
def eliminar_informe(
    informe_id: str,
    repositorio_informe: RepositorioInforme = Depends(obtener_repositorio_informe),
) -> None:
    caso_de_uso = EliminarInforme(repositorio_informe)
    caso_de_uso.ejecutar(informe_id)