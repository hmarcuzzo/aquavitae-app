from dataclasses import dataclass

from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class AnthropometricData(BaseEntity):
    weight: Float = Column(Float, nullable=True)
    height: Integer = Column(Integer, nullable=True)
    waist_circumference: Integer = Column(Integer, nullable=True)
    fat_mass: Float = Column(Float, nullable=True)
    muscle_mass: Float = Column(Float, nullable=True)
    bone_mass: Float = Column(Float, nullable=True)
    body_water: Float = Column(Float, nullable=True)
    basal_metabolism: Integer = Column(Integer, nullable=True)
    visceral_fat: Integer = Column(Integer, nullable=True)
    date: Date = Column(Date, nullable=False)
    body_photo: URLType = Column(URLType, nullable=True)

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="anthropometric_data")

    def __init__(
        self,
        date: Date,
        user_id: UUID,
        weight: Float = None,
        height: Integer = None,
        waist_circumference: Integer = None,
        fat_mass: Float = None,
        muscle_mass: Float = None,
        bone_mass: Float = None,
        body_water: Float = None,
        basal_metabolism: Integer = None,
        visceral_fat: Integer = None,
        body_photo: URLType = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.weight = weight
        self.height = height
        self.waist_circumference = waist_circumference
        self.fat_mass = fat_mass
        self.muscle_mass = muscle_mass
        self.bone_mass = bone_mass
        self.body_water = body_water
        self.basal_metabolism = basal_metabolism
        self.visceral_fat = visceral_fat
        self.date = date
        self.user_id = user_id
        self.body_photo = body_photo
