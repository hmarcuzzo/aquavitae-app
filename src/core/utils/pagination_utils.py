from typing import List, TypeVar, Union

from pydantic.main import ModelMetaclass
from sqlalchemy import inspect, or_, String
from sqlalchemy_utils import cast_if, get_columns

from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.pagination_type import Pagination, PaginationSearch, PaginationSort

E = TypeVar("E")
F = TypeVar("F")
O = TypeVar("O")
C = TypeVar("C")


class PaginationUtils:
    @staticmethod
    def generate_paging_parameters(
        skip: int,
        take: int,
        search: Union[list[str], None],
        sort: Union[list[str], None],
        find_all_query: F = None,
        order_by_query: O = None,
    ) -> Pagination:
        paging_params = Pagination(skip=skip, take=take)

        if sort:
            sort = list(set(sort))
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

            if order_by_query and not PaginationUtils.validate_sort_filter(
                paging_params["sort"], order_by_query
            ):
                raise BadRequestException("Invalid sort filters")

        paging_params["search"] = []
        if search:
            search = list(set(search))
            for search_param in search:
                search_param_split = search_param.split(":")
                paging_params["search"].append(
                    PaginationSearch(field=search_param_split[0], value=search_param_split[1])
                )

        if find_all_query and not PaginationUtils.validate_search_filter(
            paging_params["search"], find_all_query
        ):
            raise BadRequestException("Invalid search filters")

        return paging_params

    @staticmethod
    def get_paging_data(
        entity: E,
        paging_params: Pagination,
        search_all: Union[str, None],
        columns: list[str],
        columns_query: C,
        find_all_query: F = None,
    ) -> FindManyOptions:
        paging_data = FindManyOptions(
            skip=(paging_params["skip"] - 1) * paging_params["take"],
            take=paging_params["take"],
            select=[],
            where=[],
            order_by=[],
            relations=[],
        )

        if "sort" in paging_params:
            for sort_param in paging_params["sort"]:
                sort_obj = getattr(entity, sort_param["field"])
                sort_func = "asc" if (sort_param["by"] == "ASC") else "desc"
                paging_data["order_by"].append(getattr(sort_obj, sort_func)())

        if "search" in paging_params:
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

        if PaginationUtils.validate_columns(list(set(columns)), columns_query):
            paging_data, columns = PaginationUtils.generating_selected_relationships_and_columns(
                paging_data, list(set(columns)), columns_query, entity
            )
        else:
            raise BadRequestException("Invalid columns")

        return paging_data

    @staticmethod
    def validate_search_filter(search: List[PaginationSearch], find_all_query_dto: F) -> bool:
        find_all_query_dto_fields = find_all_query_dto.__fields__

        if not PaginationUtils.validate_required_search_filter(search, find_all_query_dto):
            return False

        for search_param in search:
            if search_param["field"] not in find_all_query_dto_fields:
                return False

        return True

    @staticmethod
    def validate_required_search_filter(
        search: List[PaginationSearch], find_all_query_dto: F
    ) -> bool:
        find_all_query_dto_fields = find_all_query_dto.__fields__

        for field in find_all_query_dto_fields:
            if find_all_query_dto_fields[field].required and field not in [
                search_param["field"] for search_param in search
            ]:
                return False

        return True

    @staticmethod
    def validate_sort_filter(sort: List[PaginationSort], order_by_query_dto: O) -> bool:
        query_dto_fields = order_by_query_dto.__fields__

        for sort_param in sort:
            if sort_param["field"] not in query_dto_fields or sort_param["by"] not in [
                "ASC",
                "DESC",
            ]:
                return False

        return True

    @staticmethod
    def generating_selected_relationships_and_columns(
        paging_params: FindManyOptions, columns: List[str], columns_query_dto: C, entity: E
    ) -> (FindManyOptions, List[str]):
        query_dto_fields = columns_query_dto.__fields__

        for field in query_dto_fields:
            if query_dto_fields[field].sub_fields:
                for sub_field in query_dto_fields[field].sub_fields:
                    if isinstance(sub_field.type_, ModelMetaclass) and (
                        query_dto_fields[field].required or field in columns
                    ):
                        paging_params["relations"].append(field)
                        columns.remove(field) if field in columns else None
                        for entity_relationships in inspect(inspect(entity).class_).relationships:
                            if entity_relationships.key == field:
                                columns.append(list(entity_relationships.local_columns)[0].name)

            elif query_dto_fields[field].required and field not in columns:
                columns.append(field)

        if len(paging_params["relations"]) == 0:
            del paging_params["relations"]

        paging_params["select"] += columns
        if len(paging_params["select"]) == 0:
            del paging_params["select"]

        return paging_params, columns

    @staticmethod
    def validate_columns(columns: List[str], columns_query_dto: C) -> bool:
        query_dto_fields = columns_query_dto.__fields__

        for column in columns:
            if column not in query_dto_fields:
                return False

        return True
