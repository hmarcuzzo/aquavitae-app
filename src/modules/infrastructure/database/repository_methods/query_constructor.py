from typing import TypeVar, Union

from sqlalchemy import inspect
from sqlalchemy.orm import joinedload, load_only, Query, Session

from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions

T = TypeVar("T")
E = TypeVar("E")


class QueryConstructor:
    def __init__(self, entity: T):
        self.entity = entity

    # ----------- PUBLIC METHODS -----------
    def build_query(
        self,
        db: Session,
        criteria: Union[str, int, FindOneOptions, FindManyOptions] = None,
        entity: E = None,
    ) -> Query:
        entity = entity or self.entity

        if isinstance(criteria, (str, int)):
            criteria = self.__generate_find_one_options_dict(criteria, entity)

        query = db.query(entity)

        return self.__apply_options(query, entity, criteria)

    # ----------- PRIVATE METHODS -----------
    def __apply_options(
        self,
        query: Query,
        entity: Union[T, E],
        options_dict: Union[FindOneOptions, FindManyOptions] = None,
    ) -> Query:
        if not options_dict:
            return query

        options_dict = self.__fix_options_dict(options_dict)
        query = query.enable_assertions(False)

        for key in options_dict.keys():
            if key == "select":
                query = query.options(load_only(*options_dict[key]))
            elif key == "where":
                query = query.where(*options_dict[key])
            elif key == "order_by":
                query = query.order_by(*options_dict[key])
            elif key == "skip":
                query = query.offset(options_dict[key])
            elif key == "take":
                query = query.limit(options_dict[key])
            elif key == "relations":
                query = query.options(joinedload(getattr(entity, *options_dict[key])))
            else:
                raise KeyError(f"Unknown option: {key} in FindOptions")

        return query

    @staticmethod
    def __fix_options_dict(
        options_dict: Union[FindManyOptions, FindOneOptions]
    ) -> Union[FindManyOptions, FindOneOptions]:
        for attribute in ["where", "order_by", "options"]:
            if attribute in options_dict and not isinstance(options_dict[attribute], list):
                options_dict[attribute] = [options_dict[attribute]]

        return options_dict

    @staticmethod
    def __generate_find_one_options_dict(
        criteria: Union[str, int], entity: Union[T, E]
    ) -> FindOneOptions:
        return {"where": [inspect(entity).primary_key[0] == criteria]}
