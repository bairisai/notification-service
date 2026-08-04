import uuid
from datetime import datetime

from fastapi import HTTPException, status

from app.notifications.models import (
    NotificationRequest,
    NotificationResponse,
    NotificationStatusResponse,
)
from app.notifications.store import NotificationRecord, notification_store


class NotificationService:
    @staticmethod
    def submit_notification(request: NotificationRequest) -> NotificationResponse:
        notification_id = str(uuid.uuid4())
        now = datetime.utcnow()

        notification_store.save(
            NotificationRecord(
                notification_id=notification_id,
                recipient=request.recipient.dict(),
                template=request.template,
                data=request.data,
                status="QUEUED",
                created_at=now,
                updated_at=now,
            )
        )

        return NotificationResponse(
            notification_id=notification_id,
            status="QUEUED",
            message="Notification accepted for processing.",
        )

    @staticmethod
    def get_notification_status(notification_id: str) -> NotificationStatusResponse:
        record = notification_store.get(notification_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        return NotificationStatusResponse(
            notification_id=record.notification_id,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
