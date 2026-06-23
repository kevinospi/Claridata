from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from infraestructura.configuracion.settings import obtener_settings

settings = obtener_settings()

_es_sqlite = settings.database_url.startswith("sqlite")

_connect_args = {"check_same_thread": False} if _es_sqlite else {}

engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    echo=settings.debug,
)

if _es_sqlite:

    @event.listens_for(engine, "connect")
    def _activar_pragmas_sqlite(conexion_dbapi, _) -> None:
        cursor = conexion_dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def obtener_sesion_db() -> Generator[Session, None, None]:
    sesion = SessionLocal()
    try:
        yield sesion
    except Exception:
        sesion.rollback()
        raise
    finally:
        sesion.close()