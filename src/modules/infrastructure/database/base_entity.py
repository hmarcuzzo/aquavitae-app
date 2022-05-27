import re
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import get_columns

from src.modules.infrastructure.database.base import Base


@dataclass
class BaseEntity(Base):
    __abstract__ = True
    __name__: str

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    updated_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at: DateTime = Column(DateTime, nullable=True, info={'delete_column': True})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return '_'.join(re.findall('[A-Z][^A-Z]*', self.__name__)).lower()


@event.listens_for(BaseEntity, 'before_insert')
def set_before_insert(mapper, connection, target: BaseEntity) -> None:
    now = datetime.now()

    target.created_at = now
    target.updated_at = now


@event.listens_for(BaseEntity, 'before_update', propagate=True)
def set_before_update(mapper, connection, target: BaseEntity) -> None:
    if target.deleted_at:
        target.updated_at = target.deleted_at
    else:
        target.updated_at = datetime.now()


# add filter to remove deleted entities by default every time a query of this class is executed
@event.listens_for(Engine, "before_execute", retval=True)
def no_deleted(conn, clauseelement, multiparams, params):
    if clauseelement.is_selectable:
        columns = get_columns(clauseelement.column_descriptions[0]['type'])
        for column in columns:
            if 'delete_column' in column.info:
                clauseelement.append_whereclause(column == None)

    return clauseelement, multiparams, params
