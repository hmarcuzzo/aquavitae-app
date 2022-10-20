from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class MealsOptions(BaseEntity):
    suggested_by_system: Boolean = Column(Boolean, nullable=False)

    item_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    item = relationship("Item", back_populates="meals_options")

    nutritional_plan_has_meal_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("nutritional_plan_has_meal.id", ondelete="CASCADE"),
        nullable=False,
    )
    nutritional_plan_has_meal = relationship(
        "NutritionalPlanHasMeal", back_populates="meals_options"
    )

    def __init__(
        self,
        suggested_by_system: Boolean,
        item_id: UUID,
        nutritional_plan_has_meal_id: UUID,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.suggested_by_system = suggested_by_system
        self.item_id = item_id
        self.nutritional_plan_has_meal_id = nutritional_plan_has_meal_id
