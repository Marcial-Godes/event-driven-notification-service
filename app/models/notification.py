import uuid

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from sqlalchemy.sql import func

from app.db.database import Base


class Notification(Base):

    __tablename__ = "notifications"


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
        String,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )