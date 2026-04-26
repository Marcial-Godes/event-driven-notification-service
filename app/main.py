from fastapi import FastAPI
from app.db.database import test_db

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