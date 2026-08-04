from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": None,
            "status": exc.status_code,
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "timestamp": None,
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error": "Validation Failed",
            "message": exc.errors(),
        },
    )
