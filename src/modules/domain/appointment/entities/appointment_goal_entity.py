from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class AppointmentGoal(BaseEntity):
    description: String = Column(String(1000), nullable=False)

    goal_in_appointments = relationship(
        "AppointmentHasAppointmentGoal",
        back_populates="appointment_goal",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __init__(self, description: String, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
