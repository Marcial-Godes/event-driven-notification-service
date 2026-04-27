from fastapi import FastAPI
from app.db.database import test_db
from app.db.database import Base
from app.db.database import engine

from app.models.notification import Notification

from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas.notification import NotificationCreate
from app.db.database import get_db


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


@app.post("/notifications")
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):

    new_notification = Notification(
        user_id=notification.user_id,
        channel=notification.channel,
        payload=notification.payload,
        status="pending"
    )

    db.add(new_notification)

    db.commit()

    db.refresh(new_notification)

    return {
        "id": new_notification.id,
        "status": new_notification.status
    }