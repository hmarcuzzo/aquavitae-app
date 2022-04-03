from fastapi import APIRouter

from .app_controller import app_router
from src.modules.domain import domain_router, domain_entities
from src.modules.infrastructure import infrastructure_router, infrastructure_entities


app_routers = APIRouter()

# Include App Modules Routes
app_routers.include_router(app_router)
app_routers.include_router(domain_router)
app_routers.include_router(infrastructure_router)

# Include App Entities
app_entities = infrastructure_entities + domain_entities
