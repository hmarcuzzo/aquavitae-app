from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.main import app
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.utils.database_config_test_utils import DatabaseConfigTest


class TestBaseE2E:
    db_test_utils = DatabaseConfigTest()

    base_url = "http://localhost:3000"

    # ---------------------- PUBLIC METHODS ----------------------
    async def get_no_authentication(self, route: str) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.get(route)).status_code == HTTP_401_UNAUTHORIZED

    async def get_different_required_authentication(
        self, route: str, login_payload: LoginPayloadDto
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    route,
                    headers={"Authorization": f"Bearer {login_payload.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    async def del_no_authentication(self, route: str) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.delete(route)).status_code == HTTP_401_UNAUTHORIZED

    async def del_different_required_authentication(
        self, route: str, login_payload: LoginPayloadDto
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    route,
                    headers={"Authorization": f"Bearer {login_payload.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    async def patch_no_authentication(self, route: str) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.patch(route)).status_code == HTTP_401_UNAUTHORIZED

    async def patch_different_required_authentication(
        self, route: str, login_payload: LoginPayloadDto
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    route,
                    headers={"Authorization": f"Bearer {login_payload.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN
