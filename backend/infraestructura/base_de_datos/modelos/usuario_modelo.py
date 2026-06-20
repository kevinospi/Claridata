from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
    from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
    from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo


class UsuarioModelo(AuditoriaMixin, Base):
    __tablename__ = "usuarios"

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    foto_perfil: Mapped[str | None] = mapped_column(String(500), nullable=True)

    proveedor_autenticacion: Mapped[str] = mapped_column(
        String(50), nullable=False, default="email"
    )

    google_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )

    datasets: Mapped[list["DatasetModelo"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    informes: Mapped[list["InformeModelo"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    conversaciones: Mapped[list["ConversacionModelo"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )