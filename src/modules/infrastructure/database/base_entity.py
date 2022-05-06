import re
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from src.modules.infrastructure.database.base import Base


@dataclass
class BaseEntity(Base):
    __abstract__ = True
    __name__: str

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    updated_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at: DateTime = Column(DateTime, nullable=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return '_'.join(re.findall('[A-Z][^A-Z]*', self.__name__)).lower()


@event.listens_for(BaseEntity, 'before_insert')
def set_before_insert(mapper, connection, target: BaseEntity) -> None:
    target.created_at = datetime.now()
    target.updated_at = datetime.now()


@event.listens_for(BaseEntity, 'before_update')
def set_before_update(mapper, connection, target: BaseEntity) -> None:
    target.updated_at = datetime.now()
