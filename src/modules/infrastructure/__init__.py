from fastapi import APIRouter

# Infrastructure Modules import
from .auth import auth_router
from .user import User, user_router

infrastructure_routers = APIRouter()

# Include Infrastructure Modules Routes
infrastructure_routers.include_router(auth_router)
infrastructure_routers.include_router(user_router)

# Include Infrastructure Entities
infrastructure_entities = [
    User
]
