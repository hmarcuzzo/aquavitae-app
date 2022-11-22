from fastapi import APIRouter

from .entities.anthropometric_data_entity import AnthropometricData
from .controllers.anthropometric_data_controller import anthropometric_data_router


anthropometric_data_routers = APIRouter()
anthropometric_data_routers.include_router(anthropometric_data_router)

anthropometric_data_entities = [AnthropometricData]
