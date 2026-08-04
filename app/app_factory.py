from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.config import settings
from app.common.errors import http_exception_handler, validation_exception_handler
from app.common.logging import configure_logging
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

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    return app
