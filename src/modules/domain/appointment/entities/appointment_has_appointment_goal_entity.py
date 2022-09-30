from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class AppointmentHasAppointmentGoal(BaseEntity):
    appointment_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("appointment.id", ondelete="CASCADE"), nullable=False
    )
    appointment = relationship("Appointment", back_populates="appointment_has_goals")

    appointment_goal_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("appointment_goal.id", ondelete="CASCADE"), nullable=False
    )
    appointment_goal = relationship("AppointmentGoal", back_populates="goal_in_appointments")

    def __init__(self, appointment_id: UUID, appointment_goal_id: UUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appointment_id = appointment_id
        self.appointment_goal_id = appointment_goal_id
