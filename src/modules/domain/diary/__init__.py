from fastapi import APIRouter

from .entities.diary_entity import Diary
from .controllers.diary_controller import diary_router


diary_routers = APIRouter()
diary_routers.include_router(diary_router)

diary_entities = [Diary]
