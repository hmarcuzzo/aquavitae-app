from typing import List


class BaseExceptionType(Exception):
    def __init__(self, msg: str, loc: List[str] = None, _type: str = None):
        self.msg = msg
        self.loc = loc
        self.type = _type
