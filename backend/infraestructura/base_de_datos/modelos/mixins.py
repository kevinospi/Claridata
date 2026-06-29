import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator


def _generar_uuid() -> str:
    return str(uuid.uuid4())


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


class DateTimeUTC(TypeDecorator):
    """
    Tipo de columna que garantiza que toda fecha leída desde la base de
    datos tenga tzinfo=UTC explícito, incluso en motores (como SQLite)
    que no preservan el offset de zona horaria al almacenar.
    """

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value

    def process_result_value(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value


class AuditoriaMixin:
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=_generar_uuid,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=_ahora_utc,
        nullable=False,
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=_ahora_utc,
        onupdate=_ahora_utc,
        nullable=False,
    )