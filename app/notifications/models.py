from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr


class NotificationStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    FAILED = "FAILED"


class Recipient(BaseModel):
    email: EmailStr
    name: str | None = None


class NotificationRequest(BaseModel):
    recipient: Recipient
    template: str
    data: dict[str, Any]


class NotificationResponse(BaseModel):
    notification_id: str
    status: NotificationStatus
    message: str


class NotificationStatusResponse(BaseModel):
    notification_id: str
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime