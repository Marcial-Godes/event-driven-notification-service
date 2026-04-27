from sqlalchemy import create_engine, text
from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


def test_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))