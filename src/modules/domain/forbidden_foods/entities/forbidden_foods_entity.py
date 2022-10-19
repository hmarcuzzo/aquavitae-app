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

    def __init__(
        self,
        calories_limit: Integer,
        lipids_limit: Integer,
        proteins_limit: Integer,
        carbohydrates_limit: Integer,
        period_limit: Periods,
        active: Boolean,
        user_id: UUID,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.calories_limit = calories_limit
        self.lipids_limit = lipids_limit
        self.proteins_limit = proteins_limit
        self.carbohydrates_limit = carbohydrates_limit
        self.period_limit = period_limit
        self.active = active
        self.user_id = user_id
