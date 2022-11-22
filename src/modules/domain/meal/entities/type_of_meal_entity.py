from dataclasses import dataclass

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class TypeOfMeal(BaseEntity):
    description: String = Column(String(255), nullable=False)
    calories_percentage: Float = Column(Float, nullable=True, default=0)
    lipids_percentage: Float = Column(Float, nullable=True, default=0)
    proteins_percentage: Float = Column(Float, nullable=True, default=0)
    carbohydrates_percentage: Float = Column(Float, nullable=True, default=0)

    foods = relationship(
        "FoodCanEatAt", back_populates="type_of_meal", uselist=True, cascade="all, delete-orphan"
    )
    meals_of_plan = relationship(
        "MealsOfPlan", back_populates="type_of_meal", uselist=True, cascade="all, delete-orphan"
    )

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
