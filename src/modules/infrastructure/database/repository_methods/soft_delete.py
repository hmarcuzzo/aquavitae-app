from datetime import datetime
from typing import TypeVar

from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy_utils import get_columns

from src.core.utils.database_utils import DatabaseUtils

T = TypeVar("T")


class SoftDelete:
    @staticmethod
    def soft_delete_entity(entity: T, db: Session) -> int:
        entity_class = inspect(entity).class_
        delete_column = DatabaseUtils.get_column_represent_deleted(get_columns(entity_class))
        if delete_column is None:
            raise ValueError(f'Entity "{entity_class.__name__}" has no "deleted" column')

        if not getattr(entity, delete_column.name):
            setattr(entity, delete_column.name, datetime.now())
            db.flush()

            return 1

        return 0

    # @staticmethod
    # async def soft_delete_cascade_relations(entity: T, db: Session) -> int:
    #     rowcount = 0
    #
    #     cascade_entities = DatabaseUtils.get_cascade_relations(entity)
    #     for cascade_entity in cascade_entities:
    #         result = await BaseRepository(type(cascade_entity)).soft_delete_cascade(
    #             str(cascade_entity.id), db
    #         )
    #         rowcount += result["affected"]
    #
    #     return rowcount
