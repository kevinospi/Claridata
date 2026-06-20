from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infraestructura.configuracion.settings import obtener_settings

settings = obtener_settings()

_connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def obtener_sesion_db() -> Generator[Session, None, None]:
    sesion = SessionLocal()
    try:
        yield sesion
    finally:
        sesion.close()