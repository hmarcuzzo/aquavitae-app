from fastapi import APIRouter

# Domain Modules import
from .antecedent import antecedent_entities, antecedent_routers
from .anthropometric_data import anthropometric_data_entities, anthropometric_data_routers
from .appointment import appointment_entities, appointment_routers
from .biochemical_data import biochemical_data_entities, biochemical_data_routers
from .diagnosis import diagnosis_entities, diagnosis_routers
from .food import food_entities, food_routers
from .forbidden_foods import forbidden_foods_entities, forbidden_foods_routers
from .item import item_entities, item_routers
from .meal import meal_entities, meal_routers
from .nutritional_plan import nutritional_plan_entities, nutritional_plan_routers
from .personal_data import personal_data_entities, personal_data_routers
from .plan_meals import plan_meals_entities, plan_meals_routers
from .specificity import specificity_entities, specificity_routers
from .diary import diary_entities, diary_routers


domain_routers = APIRouter()

# Include Domain Modules Routes
domain_routers.include_router(personal_data_routers)
domain_routers.include_router(anthropometric_data_routers)
domain_routers.include_router(appointment_routers)
domain_routers.include_router(food_routers)
domain_routers.include_router(antecedent_routers)
domain_routers.include_router(diagnosis_routers)
domain_routers.include_router(biochemical_data_routers)
domain_routers.include_router(specificity_routers)
domain_routers.include_router(item_routers)
domain_routers.include_router(meal_routers)
domain_routers.include_router(nutritional_plan_routers)
domain_routers.include_router(forbidden_foods_routers)
domain_routers.include_router(plan_meals_routers)
domain_routers.include_router(diary_routers)

# Include Domain Entities
domain_entities = (
    food_entities
    + personal_data_entities
    + anthropometric_data_entities
    + appointment_entities
    + antecedent_entities
    + diagnosis_entities
    + biochemical_data_entities
    + specificity_entities
    + item_entities
    + meal_entities
    + nutritional_plan_entities
    + forbidden_foods_entities
    + plan_meals_entities
    + diary_entities
)
