import uuid

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.database import Base
from app.models.enums import NotificationStatus


class Notification(Base):

    __tablename__ = "notifications"

    # En sistemas distribuidos un UUID suele encajar mejor que ids secuenciales
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default=NotificationStatus.QUEUED.value
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )