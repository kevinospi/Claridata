from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
    from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo


class DatasetModelo(AuditoriaMixin, Base):
    __tablename__ = "datasets"

    usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )

    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_archivo: Mapped[str] = mapped_column(String(10), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(500), nullable=False)
    tamaño_archivo: Mapped[int] = mapped_column(Integer, nullable=False)

    numero_filas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    numero_columnas: Mapped[int | None] = mapped_column(Integer, nullable=True)

    columnas: Mapped[list | None] = mapped_column(JSON, nullable=True)
    tipos_datos: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    usuario: Mapped["UsuarioModelo"] = relationship(back_populates="datasets")

    informe: Mapped["InformeModelo | None"] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan",
        uselist=False,
    )