from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infraestructura.base_de_datos.base import Base
from infraestructura.base_de_datos.modelos.mixins import AuditoriaMixin

if TYPE_CHECKING:
    from infraestructura.base_de_datos.modelos.conversacion_modelo import ConversacionModelo
    from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
    from infraestructura.base_de_datos.modelos.grafica_modelo import GraficaModelo
    from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo


class InformeModelo(AuditoriaMixin, Base):
    __tablename__ = "informes"

    usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dataset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    guardado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    resumen_ejecutivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    estadisticas_descriptivas: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    analisis_distribucion: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    correlaciones: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    deteccion_outliers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    hallazgos_principales: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    recomendaciones: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    conclusiones: Mapped[str | None] = mapped_column(Text, nullable=True)
    descubrimientos: Mapped[list | None] = mapped_column(JSON, nullable=True)
    interpretacion_profesional: Mapped[list | None] = mapped_column(JSON, nullable=True)

    usuario: Mapped["UsuarioModelo"] = relationship(back_populates="informes")
    dataset: Mapped["DatasetModelo"] = relationship(back_populates="informe")

    graficas: Mapped[list["GraficaModelo"]] = relationship(
        back_populates="informe",
        cascade="all, delete-orphan",
    )

    conversaciones: Mapped[list["ConversacionModelo"]] = relationship(
        back_populates="informe",
        cascade="all, delete-orphan",
    )