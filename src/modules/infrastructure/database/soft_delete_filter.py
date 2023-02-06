import contextlib
from typing import Union

from sqlalchemy import event, null
from sqlalchemy.orm import DeclarativeMeta, Query
from sqlalchemy_utils import get_columns

from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions
from src.core.utils.database_utils import DatabaseUtils


class PauseListener:
    def __init__(self):
        self.paused = False

    @contextlib.contextmanager
    def pause(self, condition: Union[FindOneOptions, FindManyOptions, bool] = True):
        self.paused = DatabaseUtils.is_with_deleted_data(condition)
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

    column = DatabaseUtils.get_column_represent_deleted(columns)
    if column is not None:
        if not DatabaseUtils.should_apply_filter(query, column):
            return query

        query = query.enable_assertions(False).where(column == null())

    return query
