from src.modules.domain.appointment.entities.appointment_has_appointment_goal_entity import (
    AppointmentHasAppointmentGoal,
)
from src.modules.infrastructure.database.base_repository import BaseRepository


class AppointmentHasAppointmentGoalRepository(BaseRepository[AppointmentHasAppointmentGoal]):
    def __init__(self):
        super().__init__(AppointmentHasAppointmentGoal)
