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

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: DateTime = Column(DateTime(timezone=True), nullable=False)
    updated_at: DateTime = Column(DateTime(timezone=True), nullable=False)
    deleted_at: DateTime = Column(
        DateTime(timezone=True), nullable=True, info={"delete_column": True}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return "_".join(re.findall("[A-Z][^A-Z]*", self.__name__)).lower()


@event.listens_for(BaseEntity, "before_insert", propagate=True)
def set_before_insert(mapper, connection, target: BaseEntity) -> None:
    if not target.created_at:
        target.created_at = datetime.now()
    if not target.updated_at or target.updated_at < target.created_at:
        target.updated_at = target.created_at


@event.listens_for(BaseEntity, "before_update", propagate=True)
def set_before_update(mapper, connection, target: BaseEntity) -> None:
    if target.deleted_at:
        target.updated_at = target.deleted_at
    else:
        target.updated_at = datetime.now()
