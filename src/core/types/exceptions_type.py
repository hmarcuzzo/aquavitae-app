from typing import List

from src.core.common.base_exception_type import BaseExceptionType


class BadRequestException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = None):
        super().__init__(msg, loc, self.__class__.__name__)


class NotFoundException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = None):
        super().__init__(msg, loc, self.__class__.__name__)


class UnauthorizedException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = None):
        super().__init__(msg, loc, self.__class__.__name__)


class ForbiddenException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = None):
        super().__init__(msg, loc, self.__class__.__name__)


class InternalServerError(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = None):
        super().__init__(msg, loc, self.__class__.__name__)
