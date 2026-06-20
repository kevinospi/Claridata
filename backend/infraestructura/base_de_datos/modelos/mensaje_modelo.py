from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo


class MensajeModelo(AuditoriaMixin, Base):
    __tablename__ = "mensajes"

    conversacion_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversaciones.id", ondelete="CASCADE"), nullable=False, index=True
    )

    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    tipo_respuesta: Mapped[str | None] = mapped_column(String(20), nullable=True)

    conversacion: Mapped["ConversacionModelo"] = relationship(back_populates="mensajes")