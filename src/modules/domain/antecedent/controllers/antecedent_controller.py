from fastapi import APIRouter

from src.modules.domain.antecedent.services.antecedent_service import AntecedentService

antecedent_router = APIRouter(tags=["Antecedent"], prefix="/antecedent")

antecedent_service = AntecedentService()
