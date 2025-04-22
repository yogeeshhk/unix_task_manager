from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.common.exceptions import (
    NotFoundException,
    BadRequestException,
    UnprocessableEntityException,
    DuplicateEntryException,
    UnauthorizedException,
    UnauthenticatedException,
)


def register_exception_handlers(app):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": str(exc)}
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )

    @app.exception_handler(UnprocessableEntityException)
    async def unprocessable_entity_handler(request: Request, exc: UnprocessableEntityException):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)}
        )

    @app.exception_handler(DuplicateEntryException)
    async def duplicate_entry_handler(request: Request, exc: DuplicateEntryException):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": str(exc)}
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": str(exc)}
        )

    @app.exception_handler(UnauthenticatedException)
    async def unauthenticated_handler(request: Request, exc: UnauthenticatedException):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."}
        )
