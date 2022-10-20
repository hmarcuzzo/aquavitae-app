from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants.enum.periods import Periods
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class NutritionalPlan(BaseEntity):
    calories_limit: Integer = Column(Integer, nullable=True, default=0)
    lipids_limit: Integer = Column(Integer, nullable=True, default=0)
    proteins_limit: Integer = Column(Integer, nullable=True, default=0)
    carbohydrates_limit: Integer = Column(Integer, nullable=True, default=0)
    period_limit: Periods = Column(Enum(Periods), nullable=False)
    active: Boolean = Column(Boolean, nullable=False)

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="nutritional_plans")

    forbidden_foods = relationship(
        "ForbiddenFoods",
        back_populates="nutritional_plan",
        uselist=True,
        cascade="all, delete-orphan",
    )
    nutritional_plan_meals = relationship(
        "NutritionalPlanHasMeal",
        back_populates="nutritional_plan",
        uselist=True,
        cascade="all, delete-orphan",
    )

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
