from typing import TypeVar, Union

from fastapi import Query

from src.core.types.find_many_options_type import FindManyOptions
from src.core.utils.pagination_utils import PaginationUtils

E = TypeVar("E")
F = TypeVar("F")
O = TypeVar("O")
C = TypeVar("C")


class GetPagination(object):
    def __init__(
        self,
        entity: E,
        columns_query: C,
        find_all_query: F = None,
        order_by_query: O = None,
    ):
        self.entity = entity
        self.columns_query = columns_query
        self.find_all_query = find_all_query
        self.order_by_query = order_by_query

    def __call__(
        self,
        skip: int = Query(default=1, ge=1),
        take: int = Query(default=10, ge=1, le=100),
        search: Union[list[str], None] = Query(
            default=None, regex=".*:.*$", example=["field:value"]
        ),
        sort: Union[list[str], None] = Query(
            default=None, regex=".*:(ASC|DESC|\\+|\\-)$", example=["field:by"]
        ),
        columns: Union[list[str], None] = Query(default=None, regex=".*", example=["field"]),
        search_all: Union[str, None] = Query(default=None),
    ) -> FindManyOptions:
        paging_params = PaginationUtils.generate_paging_parameters(
            skip,
            take,
            search,
            sort,
            self.find_all_query,
            self.order_by_query,
        )

        return PaginationUtils.get_paging_data(
            self.entity,
            paging_params,
            search_all,
            columns if columns else [],
            self.columns_query,
            self.find_all_query,
        )
