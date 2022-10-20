from dataclasses import dataclass

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class NutritionalPlanHasMeal(BaseEntity):
    meal_date: Date = Column(Date, nullable=False)

    nutritional_plan_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("nutritional_plan.id", ondelete="CASCADE"), nullable=False
    )
    nutritional_plan = relationship("NutritionalPlan", back_populates="nutritional_plan_meals")

    meals_of_plan_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("meals_of_plan.id", ondelete="CASCADE"), nullable=False
    )
    meals_of_plan = relationship("MealsOfPlan", back_populates="nutritional_plan_meals")

    def __init__(
        self,
        meal_date: Date,
        nutritional_plan_id: UUID,
        meals_of_plan_id: UUID,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.meal_date = meal_date
        self.nutritional_plan_id = nutritional_plan_id
        self.meals_of_plan_id = meals_of_plan_id
