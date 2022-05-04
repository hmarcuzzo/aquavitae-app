from fastapi import FastAPI

from src.core.handlers.http_exceptions_handler import HttpExceptionsHandler
from src.modules.app import app_routers

app = FastAPI(
    title='Aquavitae App',
    version='0.0.1'
)

# Register all routers
app.include_router(app_routers)

# Register all custom exception handler
HttpExceptionsHandler(app)

