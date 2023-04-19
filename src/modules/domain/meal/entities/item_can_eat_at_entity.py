from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class ItemCanEatAt(BaseEntity):
    type_of_meal_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("type_of_meal.id", ondelete="CASCADE"), nullable=False
    )
    type_of_meal = relationship("TypeOfMeal", back_populates="items")

    item_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    item = relationship("Item", back_populates="can_eat_at")

    def __init__(
        self,
        type_of_meal_id: UUID,
        item_id: UUID,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.type_of_meal_id = type_of_meal_id
        self.item_id = item_id
