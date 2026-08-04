from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr


class Recipient(BaseModel):
    email: EmailStr
    name: str | None = None


class NotificationRequest(BaseModel):
    recipient: Recipient
    template: str
    data: dict[str, Any]


class NotificationResponse(BaseModel):
    notification_id: str
    status: str
    message: str


class NotificationStatusResponse(BaseModel):
    notification_id: str
    status: str
    created_at: datetime
    updated_at: datetime
