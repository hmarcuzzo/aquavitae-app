from typing import Any, List, TypedDict


class FindOneOptions(TypedDict, total=False):
    select: List[str]
    where: Any
    order_by: Any
    relations: Any
    with_deleted: bool
