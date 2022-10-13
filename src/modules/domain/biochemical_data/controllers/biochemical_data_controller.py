from fastapi import APIRouter

from src.modules.domain.biochemical_data.services.biochemical_data_service import (
    BiochemicalDataService,
)

biochemical_data_router = APIRouter(tags=["Biochemical Data"], prefix="/biochemical-data")

biochemical_data_service = BiochemicalDataService()
