from typing import Any, List, Union

from sqlalchemy import Column
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions


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
