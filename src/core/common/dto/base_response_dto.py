from typing import List


class BaseResponseDto:
    def __init__(self, status_code: int, exc: List):
        self.detail = exc
        self.status_code = status_code



