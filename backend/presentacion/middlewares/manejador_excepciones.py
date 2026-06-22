from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aplicacion.excepciones import (
    AccesoDenegadoError,
    ArchivoVacioError,
    ConversacionNoEncontradaError,
    CredencialesInvalidasError,
    DatasetNoEncontradoError,
    EmailYaRegistradoError,
    ErrorAnalisisDataset,
    ErrorAplicacion,
    ExtensionNoSoportadaError,
    InformeNoEncontradoError,
    MensajeNoEncontradoError,
    TamañoArchivoExcedidoError,
    TipoConversacionInvalidoError,
    UsuarioNoEncontradoError,
)

_MAPA_CODIGOS_HTTP: dict[type[ErrorAplicacion], int] = {
    UsuarioNoEncontradoError: 404,
    DatasetNoEncontradoError: 404,
    InformeNoEncontradoError: 404,
    ConversacionNoEncontradaError: 404,
    MensajeNoEncontradoError: 404,
    EmailYaRegistradoError: 409,
    CredencialesInvalidasError: 401,
    AccesoDenegadoError: 403,
    TipoConversacionInvalidoError: 422,
    ExtensionNoSoportadaError: 422,
    ArchivoVacioError: 422,
    TamañoArchivoExcedidoError: 422,
    ErrorAnalisisDataset: 422,
}


def registrar_manejadores_excepciones(app: FastAPI) -> None:
    @app.exception_handler(ErrorAplicacion)
    def manejar_error_aplicacion(request: Request, exc: ErrorAplicacion) -> JSONResponse:
        codigo_http = _MAPA_CODIGOS_HTTP.get(type(exc), 400)
        return JSONResponse(
            status_code=codigo_http,
            content={"detalle": str(exc)},
        )