from typing import List

from src.core.common.base_exception_type import BaseExceptionType


class BadRequestException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = []):
        super().__init__(msg, loc, 'BadRequestException')


class NotFoundException(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = []):
        super().__init__(msg, loc, 'NotFoundException')


class InternalServerError(BaseExceptionType):
    def __init__(self, msg: str, loc: List[str] = []):
        super().__init__(msg, loc, 'InternalServerError')
