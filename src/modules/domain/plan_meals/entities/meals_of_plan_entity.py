from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class MealsOfPlan(BaseEntity):
    description: String = Column(String(255), nullable=False)
    start_time: Time = Column(Time(timezone=True), nullable=False, default=0)
    end_time: Time = Column(Time(timezone=True), nullable=False, default=0)

    type_of_meal_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("type_of_meal.id", ondelete="CASCADE"), nullable=False
    )
    type_of_meal = relationship("TypeOfMeal", back_populates="meals_of_plan")

    def __init__(
        self,
        description: String(255),
        start_time: Time,
        end_time: Time,
        type_of_meal_id: UUID,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.type_of_meal_id = type_of_meal_id
