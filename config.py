import os

from dotenv import load_dotenv

load_dotenv()

# --------------- DEFAULT APP CONFIGURATION --------------- #
APP_ENV = os.getenv("APP_ENV")
APP_TZ = os.getenv("APP_TZ")
APP_PORT = int(os.getenv("APP_PORT"))

# --------------- DEFAULT DATABASE CONNECTION --------------- #
DATABASE_CONNECTION = os.getenv("DATABASE_CONNECTION")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_NAME = os.getenv("DATABASE_NAME")

# --------------- DEFAULT TEST CONFIGURATIONS --------------- #
TEST_DATABASE_NAME = os.getenv("DATABASE_NAME")

# --------------- DEFAULT SECRET KEY --------------- #
TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES"))
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")
