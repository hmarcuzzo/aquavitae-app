from fastapi import APIRouter

from .entities.biochemical_data_entity import BiochemicalData
from .controllers.biochemical_data_controller import biochemical_data_router

biochemical_data_routers = APIRouter()
biochemical_data_routers.include_router(biochemical_data_router)

biochemical_data_entities = [BiochemicalData]
