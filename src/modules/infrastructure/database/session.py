from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import (
    APP_TZ,
    DATABASE_CONNECTION,
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USERNAME,
)

SQLALCHEMY_DATABASE_URL = (
    f"{DATABASE_CONNECTION}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": f"-c timezone={APP_TZ}"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
