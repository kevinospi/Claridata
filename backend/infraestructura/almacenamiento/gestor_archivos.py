import os
import uuid

DIRECTORIO_BASE = os.path.join("almacenamiento", "datasets")


class GestorArchivos:
    def __init__(self, directorio_base: str = DIRECTORIO_BASE) -> None:
        self._directorio_base = directorio_base
        os.makedirs(self._directorio_base, exist_ok=True)

    def guardar(self, nombre_archivo: str, contenido: bytes) -> str:
        extension = nombre_archivo.rsplit(".", maxsplit=1)[-1].lower()
        nombre_unico = f"{uuid.uuid4()}.{extension}"
        ruta_completa = os.path.join(self._directorio_base, nombre_unico)

        with open(ruta_completa, "wb") as archivo:
            archivo.write(contenido)

        return ruta_completa