import os
import time

from fastapi import FastAPI

from config import APP_TZ
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

# Set the default timezone of the application
os.environ['TZ'] = APP_TZ
time.tzset()
