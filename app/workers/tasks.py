import logging
import time

from sqlalchemy import update

from app.db.database import SessionLocal
from app.models.enums import NotificationStatus
from app.models.notification import Notification
from app.workers.celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="send_notification")
def send_notification(notification_id):
    db = SessionLocal()

    try:
        # El mensaje pasa de queued a processing
        db.execute(
            update(Notification)
            .where(
                Notification.id == notification_id
            )
            .values(
                status=NotificationStatus.PROCESSING.value
            )
        )

        db.commit()

        logger.info(
            "Sending notification %s",
            notification_id
        )

        # Simulamos latencia de un proveedor externo
        time.sleep(3)

        db.execute(
            update(Notification)
            .where(
                Notification.id == notification_id
            )
            .values(
                status=NotificationStatus.SENT.value
            )
        )

        db.commit()

        logger.info(
            "Notification %s sent",
            notification_id
        )

    except Exception:
        # Si algo falla limpiamos la transacción
        db.rollback()

        # Dejamos trazabilidad en base de datos
        db.execute(
            update(Notification)
            .where(
                Notification.id == notification_id
            )
            .values(
                status=NotificationStatus.FAILED.value
            )
        )

        db.commit()

        raise

    finally:
        db.close()