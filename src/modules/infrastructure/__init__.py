from fastapi import APIRouter

# Infrastructure Modules import
from src.modules.infrastructure import user

infrastructure_router = APIRouter()

# Include Infrastructure Modules Routes
infrastructure_router.include_router(user.user_router)

# Include Infrastructure Entities
infrastructure_entities = [
    user.User
]
