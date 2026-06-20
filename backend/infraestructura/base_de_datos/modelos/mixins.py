import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


def _generar_uuid() -> str:
    return str(uuid.uuid4())


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


class AuditoriaMixin:
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=_generar_uuid,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_ahora_utc,
        nullable=False,
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_ahora_utc,
        onupdate=_ahora_utc,
        nullable=False,
    )