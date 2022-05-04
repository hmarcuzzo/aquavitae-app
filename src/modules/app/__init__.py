from fastapi import APIRouter

from src.modules.domain import domain_entities, domain_routers
from src.modules.infrastructure import infrastructure_entities, infrastructure_routers
from .app_controller import app_router

app_routers = APIRouter()

# Include App Modules Routes
app_routers.include_router(app_router)
app_routers.include_router(domain_routers)
app_routers.include_router(infrastructure_routers)

# Include App Entities
app_entities = infrastructure_entities + domain_entities
