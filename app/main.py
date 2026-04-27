from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db, check_db_connection
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate
from app.workers.tasks import send_notification
from app.models.enums import NotificationStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas automáticamente en entorno local
    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "message": "service running"
    }


@app.get("/health")
def health():

    db = "down"
    error = None

    try:
        # Comprobación simple de conexión a base de datos
        check_db_connection()
        db = "up"

    except Exception as e:
        error = str(e)

    return {
        "api": "up",
        "database": db,
        "error": error
    }


@app.post(
    "/notifications",
    status_code=202
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    new_notification = Notification(
        user_id=notification.user_id,
        channel=notification.channel,
        payload=notification.payload
    )

    db.add(new_notification)

    db.commit()

    db.refresh(new_notification)

    # Encolamos el envío para procesarlo en segundo plano
    send_notification.delay(
        new_notification.id
    )

    return {
        "id": new_notification.id,
        "status": new_notification.status
    }


@app.get("/notifications/{notification_id}")
def get_notification(
    notification_id: str,
    db: Session = Depends(get_db)
):
    notification = db.get(
        Notification,
        notification_id
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "channel": notification.channel,
        "status": notification.status,
        "payload": notification.payload
    }