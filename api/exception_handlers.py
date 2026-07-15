from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.logger import app_logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    app_logger.warning(
        f"HTTP Error: {request.method} "
        f"{request.url.path} - {exc.status_code}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": str(exc.detail),
            },
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    app_logger.warning(
        f"Request validation failed: "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "success": False,
                "error": {
                    "type": "ValidationError",
                    "message": "Invalid request data",
                    "details": exc.errors(),
                },
            }
        ),
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    app_logger.exception(
        f"Unhandled API error: "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "Internal server error",
            },
        },
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        global_exception_handler,
    )