import json
from copy import deepcopy
from datetime import datetime
from typing import List, Union

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.core.common.dto.exception_response_dto import DetailResponseDto, ExceptionResponseDto
from src.core.types.exceptions_type import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from src.core.utils.json_utils import JsonUtils


class HttpExceptionsHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_exceptions_handler()

    def add_exceptions_handler(self):
        @self.app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc) -> Response:
            return Response(
                status_code=exc.status_code,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=exc.status_code,
                        detail=DetailResponseDto(loc=[], msg=exc.detail, type="starlette_http_exception"),
                        request=request,
                    ).__dict__,
                    default=JsonUtils.json_serial,
                ),
            )

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ) -> Response:
            return Response(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=[DetailResponseDto(**detail) for detail in exc.errors()],
                        request=request,
                    ).__dict__,
                    default=JsonUtils.json_serial,
                ),
            )

        @self.app.exception_handler(BadRequestException)
        @self.app.exception_handler(UnauthorizedException)
        @self.app.exception_handler(ForbiddenException)
        @self.app.exception_handler(NotFoundException)
        async def custom_exceptions_handler(
            request: Request, exc: BadRequestException
        ) -> Response:
            detail = deepcopy(exc)
            delattr(detail, "status_code")

            return Response(
                status_code=exc.status_code,
                content=json.dumps(
                    self.global_exception_error_message(
                        status_code=exc.status_code,
                        detail=DetailResponseDto(**detail.__dict__),
                        request=request,
                    ).__dict__,
                    default=JsonUtils.json_serial,
                ),
            )

    @staticmethod
    def global_exception_error_message(
        status_code: int,
        detail: Union[DetailResponseDto, List[DetailResponseDto]],
        request: Request,
    ) -> ExceptionResponseDto:
        if not isinstance(detail, List):
            detail = [detail]

        return ExceptionResponseDto(
            detail=detail,
            status_code=status_code,
            timestamp=datetime.now().astimezone(),
            path=request.url.path,
            method=request.method,
        )
