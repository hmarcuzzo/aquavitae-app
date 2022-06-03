from typing import Any, TypedDict, Union


class DeleteResult(TypedDict):
    raw: Any
    affected: Union[int, None]
