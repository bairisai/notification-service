from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NotificationRecord:
    notification_id: str
    recipient: dict[str, Any]
    template: str
    data: dict[str, Any]
    status: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class InMemoryNotificationStore:
    def __init__(self) -> None:
        self._store: dict[str, NotificationRecord] = {}

    def save(self, record: NotificationRecord) -> None:
        self._store[record.notification_id] = record

    def get(self, notification_id: str) -> NotificationRecord | None:
        return self._store.get(notification_id)


notification_store = InMemoryNotificationStore()
