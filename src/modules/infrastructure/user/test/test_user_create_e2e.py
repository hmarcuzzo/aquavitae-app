from typing import Optional

import pytest
from httpx import AsyncClient

from src.main import app
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.utils.test_base_e2e import TestBaseE2E


CONTROLLER = "user"


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllUsers(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all existing users")
    async def test_all_users(self, user_admin: Optional[LoginPayloadDto]):
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )
        assert response.status_code == 200
