from typing import Literal

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    user_id: str

    # Restringimos canales válidos en la propia entrada
    channel: Literal[
        "email",
        "sms"
    ]

    payload: dict