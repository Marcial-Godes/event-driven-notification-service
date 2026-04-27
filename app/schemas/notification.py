from pydantic import BaseModel
from typing import Literal


class NotificationCreate(BaseModel):
    user_id: str
    channel: Literal["email", "sms"]
    payload: dict