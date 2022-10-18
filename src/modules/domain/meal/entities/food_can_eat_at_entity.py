from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class FoodCanEatAt(BaseEntity):
    type_of_meal_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("type_of_meal.id", ondelete="CASCADE"), nullable=False
    )
    type_of_meal = relationship("TypeOfMeal", back_populates="foods")

    food_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food.id", ondelete="CASCADE"), nullable=False
    )
    food = relationship("Food", back_populates="can_eat_at")

    def __init__(
        self,
        type_of_meal_id: UUID,
        food_id: UUID,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.type_of_meal_id = type_of_meal_id
        self.food_id = food_id
