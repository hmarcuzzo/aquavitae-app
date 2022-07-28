from dataclasses import dataclass

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class PersonalData(BaseEntity):
    first_name: String = Column(String(255), nullable=False)
    last_name: String = Column(String(255), nullable=False)
    birthday: Date = Column(Date, nullable=False)
    occupation: String = Column(String(255), nullable=True)
    food_history: String = Column(String(1000), nullable=True)
    bedtime: Time = Column(Time(timezone=True), nullable=False)
    wake_up: Time = Column(Time(timezone=True), nullable=False)

    activity_level_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("activity_level.id"), nullable=True
    )
    activity_level = relationship("ActivityLevel", back_populates="personal_data")

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user = relationship("User", back_populates="personal_data")

    def __init__(
        self,
        first_name: String,
        last_name: String,
        birthday: DateTime,
        bedtime: Time,
        wake_up: Time,
        user_id: UUID,
        occupation: String = None,
        food_history: String = None,
        activity_level_id: UUID = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.occupation = occupation
        self.food_history = food_history
        self.bedtime = bedtime
        self.wake_up = wake_up
        self.activity_level_id = activity_level_id
        self.user_id = user_id
