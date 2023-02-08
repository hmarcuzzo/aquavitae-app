from typing import Any, List, TypeVar, Union

from sqlalchemy import Column, inspect
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList
from sqlalchemy_utils import get_columns

from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions

T = TypeVar("T")


class DatabaseUtils:
    @staticmethod
    def get_column_represent_deleted(columns: List[Column]) -> Union[Column, None]:
        for column in columns:
            if "delete_column" in column.info and column.info["delete_column"]:
                return column

        return None

    @staticmethod
    def should_apply_filter(query: Query, column: Column) -> bool:
        for clause in DatabaseUtils.get_where_clauses(query.whereclause):
            if clause.description is column.description:
                return False

        return True

    @staticmethod
    def get_where_clauses(
        whereclauses: Union[BooleanClauseList, BinaryExpression, List[Any]]
    ) -> List[Column]:
        if whereclauses is None:
            return []

        clauses = []

        if isinstance(whereclauses, BinaryExpression):
            whereclauses = [whereclauses]

        for clause in whereclauses:
            if hasattr(clause, "left"):
                clauses += DatabaseUtils.get_where_clauses([clause.left])
            elif hasattr(clause, "clause"):
                clauses += DatabaseUtils.get_where_clauses([clause.clause])
            else:
                clauses.append(clause)

        return clauses

    @staticmethod
    def is_with_deleted_data(condition: Union[FindOneOptions, FindManyOptions]) -> bool:
        is_with_deleted_data = False

        if "with_deleted" in condition:
            is_with_deleted_data = condition["with_deleted"]
            del condition["with_deleted"]

        return is_with_deleted_data

    @staticmethod
    def is_deleted(element: T) -> bool:
        result_class = type(element)
        deleted_column = DatabaseUtils.get_column_represent_deleted(get_columns(result_class))
        return getattr(element, str(deleted_column.description))

    @staticmethod
    def get_cascade_relations(entity: T) -> List[Any]:
        cascade_relations = []

        for relation in inspect(type(entity)).relationships:
            delete_column = DatabaseUtils.get_column_represent_deleted(
                get_columns(relation.mapper.class_)
            )
            if delete_column is None:
                raise ValueError(f'Relation "{relation.key}" has no "deleted" column')

            cr = getattr(entity, relation.key)
            if cr and relation.cascade.delete_orphan:
                if not isinstance(cr, List):
                    cr = [cr]

                cascade_relations.extend(
                    cascade_relation
                    for cascade_relation in cr
                    if not getattr(cascade_relation, delete_column.name, True)
                )

        return cascade_relations
