from typing import List, TypeVar, Union

from sqlalchemy import or_, String
from sqlalchemy_utils import cast_if, get_columns

from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.pagination_type import Pagination, PaginationSearch, PaginationSort

E = TypeVar("E")
T = TypeVar("T")
F = TypeVar("F")


class PaginationUtils:
    @staticmethod
    def generate_paging_parameters(
        skip: int,
        take: int,
        search: Union[list[str], None],
        sort: Union[list[str], None],
        find_all_query: T = None,
        order_by_query: F = None,
    ) -> Pagination:
        paging_params = Pagination(skip=skip, take=take)

        if sort:
            paging_params["sort"] = []
            for sort_param in sort:
                sort_param_split = sort_param.split(":")
                if sort_param_split[1] == "+":
                    sort_param_split[1] = "ASC"
                elif sort_param_split[1] == "-":
                    sort_param_split[1] = "DESC"

                paging_params["sort"].append(
                    PaginationSort(field=sort_param_split[0], by=sort_param_split[1])
                )

            if order_by_query and not PaginationUtils.validateSortFilter(
                paging_params["sort"], order_by_query
            ):
                raise BadRequestException("Invalid sort filters")

        paging_params["search"] = []
        if search:
            for search_param in search:
                search_param_split = search_param.split(":")
                paging_params["search"].append(
                    PaginationSearch(field=search_param_split[0], value=search_param_split[1])
                )

        if find_all_query and not PaginationUtils.validateSearchFilter(
            paging_params["search"], find_all_query
        ):
            raise BadRequestException("Invalid search filters")

        return paging_params

    @staticmethod
    def get_paging_data(
        entity: E,
        paging_params: Pagination,
        search: Union[list[str], None],
        sort: Union[list[str], None],
        search_all: Union[str, None],
        find_all_query: T = None,
    ) -> FindManyOptions:
        paging_data = FindManyOptions(
            skip=(paging_params["skip"] - 1) * paging_params["take"],
            take=paging_params["take"],
            where=[],
            order_by=[],
        )

        if sort:
            for sort_param in paging_params["sort"]:
                sort_obj = getattr(entity, sort_param["field"])
                sort_func = "asc" if (sort_param["by"] == "ASC") else "desc"
                paging_data["order_by"].append(getattr(sort_obj, sort_func)())

        if search:
            for search_param in paging_params["search"]:
                search_obj = getattr(entity, search_param["field"])
                paging_data["where"].append(
                    cast_if(search_obj, String).ilike(f'%{search_param["value"]}%')
                )

        if search_all:
            if find_all_query:
                where_columns = find_all_query.__fields__
            else:
                where_columns = get_columns(entity).keys()

            where_clauses = []
            for column in where_columns:
                where_clauses.append(
                    cast_if(getattr(entity, column), String).ilike(f"%{search_all}%")
                )
            paging_data["where"].append(or_(*where_clauses))

        return paging_data

    @staticmethod
    def validateSearchFilter(search: List[PaginationSearch], find_all_query_dto: T) -> bool:
        find_all_query_dto_fields = find_all_query_dto.__fields__

        if not PaginationUtils.validateRequiredSearchFilter(search, find_all_query_dto):
            return False

        for search_param in search:
            if search_param["field"] not in find_all_query_dto_fields:
                return False

        return True

    @staticmethod
    def validateRequiredSearchFilter(search: List[PaginationSearch], find_all_query_dto: T) -> bool:
        find_all_query_dto_fields = find_all_query_dto.__fields__

        for field in find_all_query_dto_fields:
            if find_all_query_dto_fields[field].required and field not in [
                search_param["field"] for search_param in search
            ]:
                return False

        return True

    @staticmethod
    def validateSortFilter(sort: List[PaginationSort], order_by_query_dto: F) -> bool:
        query_dto_fields = order_by_query_dto.__fields__

        for sort_param in sort:
            if sort_param["field"] not in query_dto_fields or sort_param["by"] not in [
                "ASC",
                "DESC",
            ]:
                return False

        return True
