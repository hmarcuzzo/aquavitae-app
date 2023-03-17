from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants.default_values import DEFAULT_AMOUNT_GRAMS
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class ItemHasFood(BaseEntity):
    amount_grams: float = Column(Float, nullable=False, default=DEFAULT_AMOUNT_GRAMS)

    item_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    item = relationship("Item", back_populates="foods")

    food_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food.id", ondelete="CASCADE"), nullable=False
    )
    food = relationship("Food", back_populates="items")

    def __init__(
        self,
        item_id: UUID,
        food_id: UUID,
        amount_grams: float = DEFAULT_AMOUNT_GRAMS,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.amount_grams = amount_grams
        self.item_id = item_id
        self.food_id = food_id
