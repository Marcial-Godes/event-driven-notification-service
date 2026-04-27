from fastapi import FastAPI
from app.db.database import test_db
from app.db.database import Base
from app.db.database import engine

from app.models.notification import Notification


app = FastAPI()


@app.get("/")
def root():
    return {"message":"service running"}


@app.get("/health")
def health():

    db="down"
    error=None

    try:
        test_db()
        db="up"

    except Exception as e:
        error=str(e)

    return {
        "api":"up",
        "database":db,
        "error":error
    }

@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )