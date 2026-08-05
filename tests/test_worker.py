from datetime import datetime, timezone

import pytest

from app.notifications.models import NotificationStatus
from app.notifications.queue.memory import InMemoryNotificationQueue
from app.notifications.store import (
    InMemoryNotificationStore,
    NotificationRecord,
)
from app.notifications.worker.worker import NotificationWorker


@pytest.mark.asyncio
async def test_worker_processes_notification() -> None:
    queue = InMemoryNotificationQueue()
    store = InMemoryNotificationStore()

    notification = NotificationRecord(
        notification_id="test-notification-1",
        recipient={
            "email": "test@example.com",
            "name": "Test User",
        },
        template="ORDER_SHIPPED",
        data={
            "orderId": "ORD-1001",
        },
        status=NotificationStatus.QUEUED,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    store.save(notification)
    await queue.enqueue(notification)

    worker = NotificationWorker(
        queue=queue,
        store=store,
    )

    await worker.process_next_notification()

    updated_notification = store.get("test-notification-1")

    assert updated_notification is not None
    assert updated_notification.status == NotificationStatus.SENT