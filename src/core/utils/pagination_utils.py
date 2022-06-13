from typing import List

from pydantic.main import ModelMetaclass

from src.core.types.pagination_type import PaginationSearch, PaginationSort


class PaginationUtils:
    @staticmethod
    def validateSearchFilter(search: List[PaginationSearch], find_all_query_dto: ModelMetaclass) -> bool:
        find_all_query_dto_fields = find_all_query_dto.__fields__

        for search_param in search:
            if search_param['field'] not in find_all_query_dto_fields:
                return False

        return True

    @staticmethod
    def validateSortFilter(sort: List[PaginationSort], order_by_query_dto: ModelMetaclass) -> bool:
        query_dto_fields = order_by_query_dto.__fields__

        for sort_param in sort:
            if sort_param['field'] not in query_dto_fields or sort_param['by'] not in ['ASC', 'DESC']:
                return False

        return True
