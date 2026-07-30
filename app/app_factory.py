from fastapi import FastAPI
from app.common.logging import configure_logging
from app.common.config import settings
from app.health.router import router as health_router
from app.notifications.router import router as notification_router

def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
    )

    app.include_router(health_router)
    app.include_router(notification_router)
    return app