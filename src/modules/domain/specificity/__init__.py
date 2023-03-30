from fastapi import APIRouter

from .entities.specificity_entity import Specificity
from .controllers.specificity_controller import specificity_router

from .entities.specificity_type_entity import SpecificityType

specificity_routers = APIRouter()
specificity_routers.include_router(specificity_router)

specificity_entities = [Specificity, SpecificityType]
