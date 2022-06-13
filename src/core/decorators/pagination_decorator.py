from typing import Union

from fastapi import Query
from pydantic.main import ModelMetaclass
from sqlalchemy import cast, String
from sqlalchemy.orm import DeclarativeMeta

from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.pagination_type import Pagination, PaginationSearch, PaginationSort
from src.core.utils.pagination_utils import PaginationUtils


class GetPagination(object):
    def __init__(
            self,
            entity: DeclarativeMeta,
            find_all_query: ModelMetaclass = None,
            group_by_query: ModelMetaclass = None
    ):
        self.entity = entity
        self.find_all_query = find_all_query
        self.order_by_query = group_by_query

    def __call__(
            self,
            skip: int = Query(default=1, ge=1),
            take: int = Query(default=10, ge=1, le=100),
            search: Union[list[str], None] = Query(default=None, regex='.*:.*$', example=['field:value']),
            sort:  Union[list[str], None] = Query(default=None, regex='.*:(ASC|DESC|\\+|\\-)$', example=['field:by']),
    ) -> FindManyOptions:
        pagination_params: Pagination = Pagination(skip=skip, take=take)

        if sort:
            pagination_params['sort'] = []
            for sort_param in sort:
                sort_param_split = sort_param.split(':')
                if sort_param_split[1] == '+':
                    sort_param_split[1] = 'ASC'
                elif sort_param_split[1] == '-':
                    sort_param_split[1] = 'DESC'

                pagination_params['sort'].append(PaginationSort(field=sort_param_split[0], by=sort_param_split[1]))

            if (
                self.order_by_query
                and not PaginationUtils.validateSortFilter(pagination_params['sort'], self.order_by_query)
            ):
                raise BadRequestException('Invalid sort filters')

        if search:
            pagination_params['search'] = []
            for search_param in search:
                search_param_split = search_param.split(':')
                pagination_params['search'].append(
                    PaginationSearch(field=search_param_split[0], value=search_param_split[1])
                )

            if (
                self.find_all_query
                and not PaginationUtils.validateSearchFilter(pagination_params['search'], self.find_all_query)
            ):
                raise BadRequestException('Invalid search filters')

        pagination_data = FindManyOptions(
            skip=(pagination_params['skip'] - 1) * pagination_params['take'],
            take=pagination_params['take']
        )

        if sort:
            pagination_data['order_by'] = []
            for sort_param in pagination_params['sort']:
                sort_obj = getattr(self.entity, sort_param['field'])
                sort_func = 'asc' if (sort_param['by'] == 'ASC') else 'desc'
                pagination_data['order_by'].append(getattr(sort_obj, sort_func)())

        if search:
            pagination_data['where'] = []
            for search_param in pagination_params['search']:
                search_obj = getattr(self.entity, search_param['field'])
                pagination_data['where'].append(cast(search_obj, String).ilike(f'%{search_param["value"]}%'))

        return pagination_data
