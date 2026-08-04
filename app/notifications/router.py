from fastapi import APIRouter, Depends, status

from app.common.config import settings
from app.common.security import validate_api_key
from app.notifications.models import (
    NotificationRequest,
    NotificationResponse,
    NotificationStatusResponse,
)
from app.notifications.service import NotificationService

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}/notifications",
    tags=["Notifications"],
)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(validate_api_key)],
)
def submit_notification(request: NotificationRequest) -> NotificationResponse:
    """Accept a notification request for asynchronous processing."""
    return NotificationService.submit_notification(request)


@router.get(
    "/{notification_id}",
    response_model=NotificationStatusResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_api_key)],
)
def get_notification_status(notification_id: str) -> NotificationStatusResponse:
    return NotificationService.get_notification_status(notification_id)
