from fastapi import APIRouter

from .entities.diagnosis_entity import Diagnosis
from .controllers.diagnosis_controller import diagnosis_router

diagnosis_routers = APIRouter()
diagnosis_routers.include_router(diagnosis_router)

diagnosis_entities = [Diagnosis]
