import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.config import settings
from app.common.dependencies import notification_worker
from app.common.errors import (
    http_exception_handler,
    validation_exception_handler,
)
from app.common.logging import configure_logging
from app.health.router import router as health_router
from app.notifications.router import router as notification_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown."""

    worker_task = asyncio.create_task(
        notification_worker.run()
    )

    try:
        yield

    finally:
        worker_task.cancel()

        try:
            await worker_task
        except asyncio.CancelledError:
            pass


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    app.include_router(health_router)
    app.include_router(notification_router)

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    return app