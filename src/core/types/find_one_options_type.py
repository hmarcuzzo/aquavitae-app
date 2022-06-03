from typing import Any, TypedDict


class FindOneOptions(TypedDict):
    where: Any
    order_by: Any
    options: Any
    relations: Any
    with_deleted: bool
