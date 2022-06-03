from datetime import datetime
from typing import Optional, TypedDict
from uuid import UUID

from pydantic import BaseModel


class BaseOptionsDto(TypedDict):
    excludeFields: bool


class BaseDto(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
