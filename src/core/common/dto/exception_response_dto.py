from typing import List

from src.core.common.dto.base_response_dto import BaseResponseDto


class ExceptionResponseDto(BaseResponseDto):
    def __init__(self, exc: List, status_code: int, timestamp: str, path: str, method: str):
        super().__init__(status_code=status_code, exc=exc)
        self.timestamp = timestamp
        self.path = path
        self.method = method
