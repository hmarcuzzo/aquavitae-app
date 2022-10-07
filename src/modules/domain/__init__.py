from fastapi import APIRouter

# Domain Modules import
from .anthropometric_data import anthropometric_data_entities, anthropometric_data_routers
from .appointment import appointment_routers, appointment_entities
from .food import food_entities, food_routers
from .personal_data import personal_data_entities, personal_data_routers

domain_routers = APIRouter()

# Include Domain Modules Routes
domain_routers.include_router(personal_data_routers)
domain_routers.include_router(anthropometric_data_routers)
domain_routers.include_router(appointment_routers)
domain_routers.include_router(food_routers)

# Include Domain Entities
domain_entities = (
    food_entities + personal_data_entities + anthropometric_data_entities + appointment_entities
)
