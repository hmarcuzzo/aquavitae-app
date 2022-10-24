from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Diary(BaseEntity):
    item_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    item = relationship("Item", back_populates="diary_meals")

    nutritional_plan_has_meal_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("nutritional_plan_has_meal.id", ondelete="CASCADE"),
        nullable=False,
    )
    nutritional_plan_has_meal = relationship("NutritionalPlanHasMeal", back_populates="diary_meals")

    def __init__(self, item_id: UUID, nutritional_plan_has_meal_id: UUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_id = item_id
        self.nutritional_plan_has_meal_id = nutritional_plan_has_meal_id
