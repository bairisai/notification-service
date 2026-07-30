from typing import Any
from pydantic import BaseModel, EmailStr

class NotificationRequest(BaseModel):
    type: str
    recipient: EmailStr
    template: str
    data: dict[str, Any]

class NotificationResponse(BaseModel):
    notification_id: str
    status: str