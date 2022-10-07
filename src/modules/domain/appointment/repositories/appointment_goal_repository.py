from src.modules.domain.appointment.entities.appointment_goal_entity import AppointmentGoal
from src.modules.infrastructure.database.base_repository import BaseRepository


class AppointmentGoalRepository(BaseRepository[AppointmentGoal]):
    def __init__(self):
        super().__init__(AppointmentGoal)
