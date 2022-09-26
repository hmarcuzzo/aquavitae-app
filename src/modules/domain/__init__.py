from fastapi import APIRouter

# Domain Modules import
from .food import Food, food_router, FoodCategory, food_category_router
from .personal_data import PersonalData, personal_data_router, ActivityLevel, activity_level_router
from .anthropometric_data import AnthropometricData, anthropometric_data_router

domain_routers = APIRouter()

# Include Domain Modules Routes
domain_routers.include_router(anthropometric_data_router)
domain_routers.include_router(food_router)
domain_routers.include_router(food_category_router)
domain_routers.include_router(activity_level_router)
domain_routers.include_router(personal_data_router)

# Include Domain Entities
domain_entities = [AnthropometricData, Food, FoodCategory, PersonalData, ActivityLevel]
