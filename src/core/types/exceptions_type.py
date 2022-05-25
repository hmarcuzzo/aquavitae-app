from src.core.common.base_exception_type import BaseExceptionType


class BadRequestException(BaseExceptionType):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundException(BaseExceptionType):
    def __init__(self, message: str):
        super().__init__(message)


class InternalServerError(BaseExceptionType):
    def __init__(self, message: str):
        super().__init__(message)
