from fastapi import APIRouter

# Domain Modules import
from .food import Food, food_router

domain_routers = APIRouter()

# Include Domain Modules Routes
domain_routers.include_router(food_router)

# Include Domain Entities
domain_entities = [Food]
