import asyncio
from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.infrastructure.auth.auth_service import AuthService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from src.modules.infrastructure.user.entities.user_entity import User
from test.utils.database_config_test_utils import DatabaseConfigTest


db_test_utils = DatabaseConfigTest()
auth_service = AuthService()


# ---------------------- PRIVATE METHODS ----------------------
async def __login_user(
    user_email: str, user_password: str = "12345678"
) -> Optional[LoginPayloadDto]:
    return await auth_service.login_user(
        OAuth2PasswordRequestForm(username=user_email, password=user_password, scope="*"),
        db_test_utils.db,
    )


# ---------------------- PRIVATE FIXTURES ----------------------
@pytest.fixture(scope="module", autouse=True)
async def __run_around_tests(request: FixtureRequest) -> None:
    fixtures_to_reload = (
        request.module.fixtures_to_reload if hasattr(request.module, "fixtures_to_reload") else None
    )

    await db_test_utils.reload_fixtures(fixtures_to_reload)

    yield

    await db_test_utils.close_db_connection()


# ---------------------- PUBLIC FIXTURES ----------------------
@pytest.fixture(scope="module")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope="module")
async def user_common() -> Optional[LoginPayloadDto]:
    user_common = db_test_utils.get_entity_objects(User)[0]
    return await __login_user(user_common["email"])


@pytest.fixture(scope="module")
async def user_nutritionist() -> Optional[LoginPayloadDto]:
    user_nutri = db_test_utils.get_entity_objects(User)[1]
    return await __login_user(user_nutri["email"])


@pytest.fixture(scope="module")
async def user_admin() -> Optional[LoginPayloadDto]:
    user_admin = db_test_utils.get_entity_objects(User)[2]
    return await __login_user(user_admin["email"])
