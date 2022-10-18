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
        description: String(255),
        calories_percentage: Float,
        lipids_percentage: Float,
        proteins_percentage: Float,
        carbohydrates_percentage: Float,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.description = description
        self.calories_percentage = calories_percentage
        self.lipids_percentage = lipids_percentage
        self.proteins_percentage = proteins_percentage
        self.carbohydrates_percentage = carbohydrates_percentage
