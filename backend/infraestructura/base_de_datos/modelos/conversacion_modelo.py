from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
    from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
    from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo


class ConversacionModelo(AuditoriaMixin, Base):
    __tablename__ = "conversaciones"

    usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    informe_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("informes.id", ondelete="CASCADE"), nullable=True, index=True
    )

    tipo_conversacion: Mapped[str] = mapped_column(String(20), nullable=False)

    usuario: Mapped["UsuarioModelo"] = relationship(back_populates="conversaciones")
    informe: Mapped["InformeModelo | None"] = relationship(back_populates="conversaciones")

    mensajes: Mapped[list["MensajeModelo"]] = relationship(
        back_populates="conversacion",
        cascade="all, delete-orphan",
        order_by="MensajeModelo.fecha_creacion",
    )