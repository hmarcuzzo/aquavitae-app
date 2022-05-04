from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.core.common.base_entity import BaseEntity


class BaseDtoOptions:
    def __init__(self, excludeFields: bool = False):
        self.excludeFields = excludeFields


class BaseDto:
    id: UUID
    created_at: DateTime
    updated_at: DateTime
    deleted_at: DateTime

    def __init__(self, entity: BaseEntity, options: BaseDtoOptions = None):
        if not options or not options.excludeFields:
            self.id = entity.id
            self.created_at = entity.created_at
            self.updated_at = entity.updated_at
            self.deleted_at = entity.deleted_at
