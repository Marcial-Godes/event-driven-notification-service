from enum import Enum


# Centralizamos estados para evitar strings sueltos por el proyecto
class NotificationStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"