class ErrorAplicacion(Exception):
    pass


class UsuarioNoEncontradoError(ErrorAplicacion):
    pass


class EmailYaRegistradoError(ErrorAplicacion):
    pass


class DatasetNoEncontradoError(ErrorAplicacion):
    pass


class InformeNoEncontradoError(ErrorAplicacion):
    pass


class ConversacionNoEncontradaError(ErrorAplicacion):
    pass


class TipoConversacionInvalidoError(ErrorAplicacion):
    pass