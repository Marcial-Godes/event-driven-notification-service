from celery import Celery
from app.core.config import settings

# La configuración sale del .env para no hardcodear conexiones
celery_app = Celery(
    "notifications",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)