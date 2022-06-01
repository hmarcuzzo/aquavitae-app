import json
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Request, Response
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.core.common.dto.detail_response_dto import DetailResponseDto
from src.core.common.dto.exception_response_dto import ExceptionResponseDto
from src.core.types.exceptions_type import BadRequestException, InternalServerError, NotFoundException


class HttpExceptionsHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_exceptions_handler()

    def add_exceptions_handler(self):
        @self.app.exception_handler(BadRequestException)
        async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> Response:
            return Response(
                status_code=HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=HTTP_400_BAD_REQUEST,
                        exc=exc,
                        request=request,
                    ).__dict__
                )
            )

        @self.app.exception_handler(NotFoundException)
        async def not_found_exception_handler(request: Request, exc: NotFoundException) -> Response:
            return Response(
                status_code=HTTP_404_NOT_FOUND,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=HTTP_404_NOT_FOUND,
                        exc=exc,
                        request=request,
                    ).__dict__
                )
            )

        @self.app.exception_handler(InternalServerError)
        async def internal_server_error_exception_handler(
                request: Request,
                exc: InternalServerError
        ) -> Response:
            return Response(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        exc=exc,
                        request=request,
                    ).__dict__
                )
            )

    @staticmethod
    def global_exception_error_message(
            status_code: int, exc: Any, request: Request,
    ) -> ExceptionResponseDto:
        return ExceptionResponseDto(
            status_code=status_code,
            exc=[DetailResponseDto(element).__dict__ for element in [exc]],
            timestamp=str(datetime.now().astimezone()),
            path=request.url.path,
            method=request.method,
        )
