from typing import Generic, List, Type, TypeVar, Union

from pydantic import Extra
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationResponseDto(GenericModel, Generic[T]):
    data: List[T]
    count: int
    limit: int
    current_page: int
    next_page: Union[int, None]
    prev_page: Union[int, None]
    last_page: int

    class Config:
        extra = Extra.forbid


def create_pagination_response_dto(
    data: List[Type[T]], total: int, skip: int, limit: int
) -> PaginationResponseDto:
    current_page = skip // limit + 1
    prev_page = current_page - 1 if current_page > 1 else None
    last_page = (
        (total // limit if total // limit > 0 else total // limit + 1)
        if total % limit == 0
        else total // limit + 1
    )
    next_page = current_page + 1 if current_page < last_page else None

    return PaginationResponseDto(
        data=data,
        count=total,
        limit=limit,
        current_page=current_page,
        prev_page=prev_page,
        last_page=last_page,
        next_page=next_page,
    )
