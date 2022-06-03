import contextlib

from sqlalchemy import event
from sqlalchemy.orm import DeclarativeMeta, Query
from sqlalchemy.sql.elements import BinaryExpression
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
    columns = [] if not isinstance(query.column_descriptions[0]['entity'], DeclarativeMeta) \
        else get_columns(query.column_descriptions[0]['entity'])

    for column in columns:
        if 'delete_column' in column.info and column.info['delete_column']:
            if not __should_apply_filter(query, column):
                return query

            query = query.enable_assertions(False).where(column == None)
            break

    return query


def __should_apply_filter(query: Query, column) -> bool:
    for clause in __get_where_clauses(query):
        if clause.left.description is column.description:
            return False

    return True


def __get_where_clauses(query: Query) -> list[BinaryExpression]:
    if hasattr(query.whereclause, 'clauses'):
        return [clause for clause in query.whereclause.clauses]
    else:
        if query.whereclause is not None:
            return [query.whereclause]
        return []
