from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException, status

from app.notifications.models import (
    NotificationRequest,
    NotificationResponse,
    NotificationStatus,
    NotificationStatusResponse,
)
from app.common.dependencies import (
    notification_queue, 
    notification_store,
    )
from app.notifications.store import NotificationRecord
    


class NotificationService:

    @staticmethod
    async def submit_notification(
        request: NotificationRequest,
    ) -> NotificationResponse:
        """Accept and enqueue a notification request."""

        notification_id = str(uuid4())
        now = datetime.now(timezone.utc)

        record = NotificationRecord(
            notification_id=notification_id,
            recipient=request.recipient.model_dump(),
            template=request.template,
            data=request.data,
            status=NotificationStatus.QUEUED,
            created_at=now,
            updated_at=now,
        )

        notification_store.save(record)

        await notification_queue.enqueue(record)

        return NotificationResponse(
            notification_id=notification_id,
            status=NotificationStatus.QUEUED,
            message="Notification accepted for processing.",
        )

    @staticmethod
    def get_notification_status(
        notification_id: str,
    ) -> NotificationStatusResponse:
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