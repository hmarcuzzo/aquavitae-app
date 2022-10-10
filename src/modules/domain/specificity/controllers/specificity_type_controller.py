from fastapi import APIRouter

from src.modules.domain.specificity.services.specificity_type_service import SpecificityTypeService

specificity_type_router = APIRouter(tags=["Specificity Type"], prefix="/specificity-type")

specificity_type_service = SpecificityTypeService()
