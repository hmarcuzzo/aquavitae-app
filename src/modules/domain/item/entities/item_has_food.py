from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class ItemHasFood(BaseEntity):
    amount_grams: Float = Column(Float, nullable=False)

    item_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    item = relationship("Item", back_populates="foods")

    food_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food.id", ondelete="CASCADE"), nullable=False
    )
    food = relationship("Food", back_populates="items")

    def __init__(self, amount_grams: Float, item_id: UUID, food_id: UUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount_grams = amount_grams
        self.item_id = item_id
        self.food_id = food_id
