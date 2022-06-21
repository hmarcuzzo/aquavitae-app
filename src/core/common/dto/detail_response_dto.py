from src.core.common.base_exception_type import BaseExceptionType


class DetailResponseDto:
    def __init__(self, exc: BaseExceptionType):
        self.loc = exc.loc
        self.msg = exc.msg
        self.type = exc.type
