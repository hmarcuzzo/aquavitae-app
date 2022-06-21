from typing import Any, TypedDict


class FindOneOptions(TypedDict):
    where: Any
    order_by: Any
    relations: Any
    with_deleted: bool
