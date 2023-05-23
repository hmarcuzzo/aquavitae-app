from datetime import datetime
from typing import Optional, TypedDict
from uuid import UUID

from pydantic import BaseModel


class BaseOptionsDto(TypedDict):
    excludeFields: bool


class BaseDto(BaseModel):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    def __hash__(self):
        return hash(self.id)
