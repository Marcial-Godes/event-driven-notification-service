from sqlalchemy import create_engine, text
from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={
        "client_encoding": "utf8"
    }
)


def test_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))