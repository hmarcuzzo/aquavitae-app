import asyncio
from typing import Optional

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.main import app
from src.modules.infrastructure.auth.auth_service import AuthService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from src.modules.infrastructure.user.entities.user_entity import User
from test.utils.database_config_test_utils import DatabaseConfigTest


class TestBaseE2E:
    db_test_utils = DatabaseConfigTest()
    auth_service = AuthService()

    base_url = "http://localhost:3000"
    fixtures_to_reload = None

    # ---------------------- PRIVATE METHODS ----------------------
    async def __login_user(
        self, user_email: str, user_password: str = "12345678"
    ) -> Optional[LoginPayloadDto]:
        return await self.auth_service.login_user(
            OAuth2PasswordRequestForm(username=user_email, password=user_password, scope="*"),
            self.db_test_utils.db,
        )

    # ---------------------- PUBLIC METHODS ----------------------
    async def no_authentication(self, route: str) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.get(route)).status_code == HTTP_401_UNAUTHORIZED

    async def different_required_authentication(
        self, route: str, login_payload: LoginPayloadDto
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    route,
                    headers={"Authorization": f"Bearer {login_payload.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    # ---------------------- PRIVATE FIXTURES ----------------------
    @pytest.fixture(scope="module", autouse=True)
    async def __run_around_tests(self) -> None:
        await self.db_test_utils.reload_fixtures(self.fixtures_to_reload)

        yield

        await self.db_test_utils.close_db_connection()

    # ---------------------- PUBLIC FIXTURES ----------------------
    @pytest.fixture(scope="module")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_event_loop()

    @pytest.fixture(scope="module")
    async def user_common(self) -> Optional[LoginPayloadDto]:
        user_common = self.db_test_utils.get_entity_objects(User)[0]
        return await self.__login_user(user_common["email"])

    @pytest.fixture(scope="module")
    async def user_nutricionist(self) -> Optional[LoginPayloadDto]:
        user_nutri = self.db_test_utils.get_entity_objects(User)[1]
        return await self.__login_user(user_nutri["email"])

    @pytest.fixture(scope="module")
    async def user_admin(self) -> Optional[LoginPayloadDto]:
        user_admin = self.db_test_utils.get_entity_objects(User)[2]
        return await self.__login_user(user_admin["email"])