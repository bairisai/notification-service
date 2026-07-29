from fastapi import APIRouter, status

from app.health.service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", status_code=status.HTTP_200_OK,)
def health_check() -> dict[str, str]:
    """Returns the health status of the application."""
    return HealthService.get_health()