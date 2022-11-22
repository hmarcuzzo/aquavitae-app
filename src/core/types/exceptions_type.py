from typing import List

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from src.core.common.base_exception_type import BaseExceptionType


class BadRequestException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = [], _type: str = None):
        if _type is None:
            _type = "bad_request"

        self.status_code = HTTP_400_BAD_REQUEST
        super().__init__(msg, loc, _type)


class UnauthorizedException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = [], _type: str = None):
        if _type is None:
            _type = "unauthorized"

        self.status_code = HTTP_401_UNAUTHORIZED
        super().__init__(msg, loc, _type)


class ForbiddenException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = [], _type: str = None):
        if _type is None:
            _type = "forbidden"

        self.status_code = HTTP_403_FORBIDDEN
        super().__init__(msg, loc, _type)


class NotFoundException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = [], _type: str = None):
        if _type is None:
            _type = "not_found"

        self.status_code = HTTP_404_NOT_FOUND
        super().__init__(msg, loc, _type)
