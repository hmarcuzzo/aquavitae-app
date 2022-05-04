import datetime
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class BaseEntity:
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at: DateTime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    deleted_at: DateTime = Column(DateTime, nullable=True)
