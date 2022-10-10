from fastapi import APIRouter

from src.modules.domain.antecedent.services.antecedent_type_service import AntecedentTypeService

antecedent_type_router = APIRouter(tags=["Antecedent Type"], prefix="/antecedent-type")

antecedent_type_service = AntecedentTypeService()
