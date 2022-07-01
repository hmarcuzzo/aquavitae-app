import json
from typing import Dict

from fastapi import FastAPI
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.core.common.dto.exception_response_dto import DetailResponseDto
from src.core.handlers.http_exceptions_handler import HttpExceptionsHandler


class AllHttpExceptionsFilter:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_exceptions_filter()

    def is_exception_response(self, body: Dict) -> bool:
        return "timestamp" in body and "path" in body and "method" in body

    def add_exceptions_filter(self):
        @self.app.middleware("http")
        async def all_http_exceptions_filter(
            request: Request, call_next: RequestResponseEndpoint
        ) -> Response:
            try:
                response = await call_next(request)

                if 400 <= response.status_code < 500:
                    body = [section async for section in response.__dict__["body_iterator"]]
                    response_body_json = json.loads(body[0].decode(response.charset))

                    if not self.is_exception_response(response_body_json):
                        result = HttpExceptionsHandler.global_exception_error_message(
                            response.status_code,
                            [DetailResponseDto(**detail) for detail in response_body_json["detail"]],
                            request,
                        ).__dict__
                    else:
                        result = response_body_json

                    return Response(
                        status_code=response.status_code, content=json.dumps(result)
                    )

            except Exception as err:
                raise err

            return response
