from fastapi import APIRouter

from src.modules.domain.specificity.services.specificity_service import SpecificityService

specificity_router = APIRouter(tags=["Specificity"], prefix="/specificity")

specificity_service = SpecificityService()
