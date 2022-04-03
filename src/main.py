from fastapi import FastAPI

from src.modules.app import app_routers

app = FastAPI(title='Aquavitae App',
              version='0.0.1')

app.include_router(app_routers)
