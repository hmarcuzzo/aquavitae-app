from typing import Any, TypedDict, Union


class UpdateResult(TypedDict):
    raw: Any
    affected: Union[int, None]
    generatedMaps: Any
