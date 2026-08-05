from typing import Protocol

from app.notifications.store import NotificationRecord


class NotificationQueue(Protocol):
    async def enqueue(self, notification: NotificationRecord) -> None:
        """Add a notification to the queue."""

    async def dequeue(self) -> NotificationRecord:
        """Remove and return the next notification."""