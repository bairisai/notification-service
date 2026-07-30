import uuid

from app.notifications.models import (
    NotificationRequest,
    NotificationResponse,
)

class NotificationService:
    @staticmethod
    def submit_notification(
            request: NotificationRequest,
    ) -> NotificationResponse:
        """Accept a notification request."""

        return NotificationResponse(
            notification_id=str(uuid.uuid4()),
            status="QUEUED",
        )