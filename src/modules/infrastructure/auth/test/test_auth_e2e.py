from typing import Optional

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.core.constants.enum.user_role import UserRole
from src.main import app
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.utils.test_base_e2e import TestBaseE2E


@pytest.mark.describe(f"GET Route: /login")
class TestGetAllUsers(TestBaseE2E):
    route = f"/login"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Login with valid credentials")
    async def test_valid_login(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route, data={"username": "henrique_user@gmail.com", "password": "12345678"}
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert [
            hasattr(data, attr_name)
            for attr_name in ["user", "expires_in", "access_token", "token_type"]
        ]
        assert data["token_type"] == "Bearer"
        assert data["user"]["email"] == "henrique_user@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Login a second time with valid credentials")
    async def test_valid_login(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route, data={"username": "henrique_user@gmail.com", "password": "12345678"}
                )
            ).status_code == HTTP_200_OK

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Login with wrong password")
    async def test_valid_login(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route, data={"username": "henrique_user@gmail.com", "password": "1234"}
                )
            ).status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Login with wrong username")
    async def test_valid_login(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route, data={"username": "henrique_user@hotmail.com", "password": "1234"}
                )
            ).status_code == HTTP_404_NOT_FOUND


@pytest.mark.describe(f"GET Route: /me")
class TestGetUserById(TestBaseE2E):
    route = f"/me"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get user admin data")
    async def test_get_current_user(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == "09cdf815-9cda-4a87-8ae9-34c06f915278"
        assert data["role"] == UserRole.ADMIN.value
        assert data["email"] == "henrique_admin@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get current user without authentication")
    async def test_no_authentication(self) -> None:
        await self.no_authentication(self.route)
