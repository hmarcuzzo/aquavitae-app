from typing import Any, List, Union

from sqlalchemy import Column
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList


class DatabaseUtils:
    @staticmethod
    def get_column_represent_deleted(columns: List[Column]) -> Column:
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
            whereclause: Union[BooleanClauseList, BinaryExpression, List[Any]]
    ) -> List[Column]:
        clauses = []

        if whereclause is not None:
            if not (
                    isinstance(whereclause, BooleanClauseList) or isinstance(whereclause, List)
            ):
                whereclause = [whereclause]

            for clause in whereclause:
                if hasattr(clause, "left"):
                    clauses += DatabaseUtils.get_where_clauses([clause.left])
                elif hasattr(clause, "clause"):
                    clauses += DatabaseUtils.get_where_clauses([clause.clause])
                else:
                    clauses.append(clause)

        return clauses