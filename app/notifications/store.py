from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.notifications.models import NotificationStatus


@dataclass
class NotificationRecord:
    notification_id: str
    recipient: dict[str, Any]
    template: str
    data: dict[str, Any]
    status: NotificationStatus
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class InMemoryNotificationStore:
    def __init__(self) -> None:
        self._store: dict[str, NotificationRecord] = {}

    def save(self, record: NotificationRecord) -> None:
        self._store[record.notification_id] = record

    def get(self, notification_id: str) -> NotificationRecord | None:
        return self._store.get(notification_id)
    
    def update_status(self, notification_id: str, status: NotificationStatus) -> None:
        record = self.get(notification_id)

        if record is None:
            raise KeyError(
                f"Notification {notification_id} not found."
            )

        record.status = status
        record.updated_at = datetime.now(timezone.utc)
        self.save(record)


