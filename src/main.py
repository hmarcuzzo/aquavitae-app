import os
import time

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import APP_ENV, APP_PORT, APP_TZ, CORS_ORIGINS
from src.core.common.custom_error_response import custom_error_response
from src.core.handlers.http_exceptions_handler import HttpExceptionsHandler
from src.core.middlewares.limit_upload_size import LimitUploadSize
from src.modules.app import app_routers

app = FastAPI(title="Aquavitae App", version="0.0.1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)  # ~50MB

# Register all custom exception handler
HttpExceptionsHandler(app)

# Set the default timezone of the application
os.environ["TZ"] = APP_TZ
time.tzset()

# Register all routers
app.include_router(app_routers)

# Modifies the error response pattern
custom_error_response(app)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=APP_PORT,
        reload=bool(APP_ENV != "production"),
        use_colors=True,
    )
