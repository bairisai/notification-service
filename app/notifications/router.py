from fastapi import APIRouter, status
from app.notifications.models import (
    NotificationRequest,
    NotificationResponse,
)

from app.notifications.service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

@router.post(
        "",
        response_model=NotificationResponse,
        status_code=status.HTTP_202_ACCEPTED,
        )
def submit_notificaiton(request: NotificationRequest,) -> NotificationResponse:
    """Accept a notification request for asynchronous processing."""
    return NotificationService.submit_notification(request)