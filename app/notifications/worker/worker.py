import asyncio
from app.notifications.queue.memory import InMemoryNotificationQueue
from app.notifications.store import InMemoryNotificationStore
from app.notifications.models import NotificationStatus

class NotificationWorker:

    def __init__(self, queue: InMemoryNotificationQueue, store: InMemoryNotificationStore) -> None:
        self._queue = queue
        self._store = store

    async def process_next_notification(self) -> None:

        notification = await self._queue.dequeue()
        self._store.update_status(notification.notification_id, NotificationStatus.PROCESSING)

        try:
            await asyncio.sleep(2)  # Simulate sending the notification (short in tests)
            self._store.update_status(notification.notification_id, NotificationStatus.SENT)

        finally:
            self._queue.task_done()
    async def run(self) -> None:
        while True:
            await self.process_next_notification()


    