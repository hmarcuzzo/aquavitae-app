from fastapi import APIRouter

from .entities.activity_level_entity import ActivityLevel
from .controllers.activity_level_controller import activity_level_router

from .entities.personal_data_entity import PersonalData
from .controllers.personal_data_controller import personal_data_router


personal_data_routers = APIRouter()
personal_data_routers.include_router(activity_level_router)
personal_data_routers.include_router(personal_data_router)

personal_data_entities = [ActivityLevel, PersonalData]
