from fastapi import APIRouter

from .entities.appointment_goal_entity import AppointmentGoal
from .controllers.appointment_goal_controller import appointment_goal_router


appointment_routers = APIRouter()
appointment_routers.include_router(appointment_goal_router)

appointment_entities = [AppointmentGoal]
