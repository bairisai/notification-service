import asyncio

from app.notifications.store import NotificationRecord


class InMemoryNotificationQueue:

    def __init__(self) -> None:
        self._queue: asyncio.Queue[NotificationRecord] = asyncio.Queue()

    async def enqueue(self, notification: NotificationRecord) -> None:
        await self._queue.put(notification)

    async def dequeue(self) -> NotificationRecord:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()

    def qsize(self) -> int:
        return self._queue.qsize()


