from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo


class GraficaModelo(AuditoriaMixin, Base):
    __tablename__ = "graficas"

    informe_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("informes.id", ondelete="CASCADE"), nullable=False, index=True
    )

    tipo_grafica: Mapped[str] = mapped_column(String(50), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    ruta_imagen: Mapped[str] = mapped_column(String(500), nullable=False)

    informe: Mapped["InformeModelo"] = relationship(back_populates="graficas")