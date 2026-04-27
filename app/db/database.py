from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


# Fábrica de sesiones para cada petición
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base común para modelos ORM
Base = declarative_base()


def check_db_connection():
    # Consulta mínima para validar conectividad
    with engine.connect() as conn:
        conn.execute(
            text("SELECT 1")
        )


def get_db():
    # Una sesión por request; FastAPI la libera al terminar
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()