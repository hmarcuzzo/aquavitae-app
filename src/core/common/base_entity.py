import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, event
from sqlalchemy.dialects.postgresql import UUID

from src.modules.infrastructure.database import Base


class BaseEntity(Base):
    __abstract__ = True

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    updated_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at: DateTime = Column(DateTime, nullable=True)


@event.listens_for(BaseEntity, 'before_insert')
def set_created_at(mapper, connection, target: BaseEntity) -> None:
    target.created_at = datetime.now()
    target.updated_at = datetime.now()


@event.listens_for(BaseEntity, 'before_update')
def set_before_update(mapper, connection, target: BaseEntity) -> None:
    target.updated_at = datetime.now()
