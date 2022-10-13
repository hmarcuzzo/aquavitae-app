from fastapi import APIRouter

from src.modules.domain.diagnosis.services.diagnosis_service import DiagnosisService

diagnosis_router = APIRouter(tags=["Diagnosis"], prefix="/diagnosis")

diagnosis_service = DiagnosisService()
