from typing import Union

from src.core.types.exceptions_type import BadRequestException, InternalServerError, NotFoundException


class DetailResponseDto:
    def __init__(self, exc: Union[BadRequestException, NotFoundException, InternalServerError]):
        self.loc = exc.loc
        self.msg = exc.msg
        self.type = exc.type
