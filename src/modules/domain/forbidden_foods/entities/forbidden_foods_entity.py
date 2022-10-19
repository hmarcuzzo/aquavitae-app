from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants.enum.periods import Periods
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class ForbiddenFoods(BaseEntity):
    food_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food.id", ondelete="CASCADE"), nullable=False
    )
    food = relationship("Food", back_populates="forbidden_in_nutritional_plans")

    nutritional_plan_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("nutritional_plan.id", ondelete="CASCADE"), nullable=False
    )
    nutritional_plan = relationship("NutritionalPlan", back_populates="forbidden_foods")

    def __init__(self, food_id: UUID, nutritional_plan_id: UUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.food_id = food_id
        self.nutritional_plan_id = nutritional_plan_id
