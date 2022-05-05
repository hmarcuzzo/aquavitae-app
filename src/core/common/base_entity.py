from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class BaseEntity:
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    updated_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    created_at: DateTime = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at: DateTime = Column(DateTime, nullable=True)
