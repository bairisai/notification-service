import logging

from app.common.config import settings

def configure_logging() -> None:
    """Configure application logging."""

    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )