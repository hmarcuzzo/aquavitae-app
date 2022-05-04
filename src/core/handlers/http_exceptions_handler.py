from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.core.types.exceptions_type import BadRequestException, NotFoundException


class HttpExceptionsHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_exceptions_handler()

    def add_exceptions_handler(self):
        @self.app.exception_handler(BadRequestException)
        async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> JSONResponse:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"message": exc.message},
            )

        @self.app.exception_handler(NotFoundException)
        async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
            return JSONResponse(
                status_code=HTTP_404_NOT_FOUND,
                content={"message": exc.message},
            )
