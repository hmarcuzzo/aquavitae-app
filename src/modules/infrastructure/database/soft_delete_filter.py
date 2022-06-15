import contextlib
from typing import Any, List, Union

from sqlalchemy import Column, event
from sqlalchemy.orm import DeclarativeMeta, Query
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList
from sqlalchemy_utils import get_columns


class PauseListener:
    def __init__(self):
        self.paused = False

    @contextlib.contextmanager
    def pause(self, condition: bool = True):
        self.paused = condition
        yield
        self.paused = False

    def __call__(self, fn):
        def run_fn(*arg, **kw):
            if not self.paused:
                return fn(*arg, **kw)

        return run_fn


pause_listener = PauseListener()


# add filter to remove deleted entities by default every time a query of this class is executed
@event.listens_for(Query, "before_compile", retval=True)
@pause_listener
def no_deleted(query: Query) -> Query:
    columns = (
        []
        if not isinstance(query.column_descriptions[0]["entity"], DeclarativeMeta)
        else get_columns(query.column_descriptions[0]["entity"])
    )

    for column in columns:
        if "delete_column" in column.info and column.info["delete_column"]:
            if not __should_apply_filter(query, column):
                return query

            query = query.enable_assertions(False).where(column == None)
            break

    return query


def __should_apply_filter(query: Query, column: Column) -> bool:
    for clause in __get_where_clauses(query.whereclause):
        if clause.description is column.description:
            return False

    return True


def __get_where_clauses(
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
                clauses += __get_where_clauses([clause.left])
            elif hasattr(clause, "clause"):
                clauses += __get_where_clauses([clause.clause])
            else:
                clauses.append(clause)

    return clauses
