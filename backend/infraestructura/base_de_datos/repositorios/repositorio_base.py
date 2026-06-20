from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from infraestructura.base_de_datos.base import Base

ModeloORM = TypeVar("ModeloORM", bound=Base)


class RepositorioBase(Generic[ModeloORM]):
    def __init__(self, sesion: Session, modelo: type[ModeloORM]) -> None:
        self._sesion = sesion
        self._modelo = modelo

    def obtener_por_id(self, id: str) -> ModeloORM | None:
        return self._sesion.get(self._modelo, id)

    def listar(self, limite: int = 100, desplazamiento: int = 0) -> list[ModeloORM]:
        return list(
            self._sesion.query(self._modelo)
            .offset(desplazamiento)
            .limit(limite)
            .all()
        )

    def crear(self, instancia: ModeloORM) -> ModeloORM:
        self._sesion.add(instancia)
        self._sesion.flush()
        return instancia

    def actualizar(self, instancia: ModeloORM) -> ModeloORM:
        self._sesion.flush()
        return instancia

    def eliminar(self, instancia: ModeloORM) -> None:
        self._sesion.delete(instancia)
        self._sesion.flush()

    def guardar_cambios(self) -> None:
        self._sesion.commit()