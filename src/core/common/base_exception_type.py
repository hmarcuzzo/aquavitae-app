from typing import List


class BaseExceptionType(Exception):
    def __init__(self, msg: str, loc: List[str] = None, type_: str = None):
        self.msg = msg
        self.loc = loc
        self.type = type_
