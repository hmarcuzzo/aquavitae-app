from fastapi import APIRouter, status

from . import app_service

app_router = APIRouter(tags=['App'])

app_service = app_service.AppService()


@app_router.get('/health-check', status_code=status.HTTP_200_OK)
def get_health() -> str:
    return app_service.health_check()
