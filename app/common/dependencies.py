from app.notifications.queue.memory import InMemoryNotificationQueue
from app.notifications.store import InMemoryNotificationStore
from app.notifications.worker.worker import NotificationWorker

notification_store = InMemoryNotificationStore()
notification_queue = InMemoryNotificationQueue()

notification_worker = NotificationWorker(
    queue=notification_queue,
    store=notification_store
)