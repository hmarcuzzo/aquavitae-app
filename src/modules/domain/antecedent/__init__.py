from fastapi import APIRouter

from .entities.antecedent_entity import Antecedent
from .controllers.antecedent_controller import antecedent_router

from .entities.antecedent_type_entity import AntecedentType
from .controllers.antecedent_type_controller import antecedent_type_router

antecedent_routers = APIRouter()
antecedent_routers.include_router(antecedent_router)
antecedent_routers.include_router(antecedent_type_router)

antecedent_entities = [Antecedent, AntecedentType]
