from datetime import date, datetime
from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.anthropometric_data.services.anthropometric_data_service import (
    AnthropometricDataService,
)
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "anthropometric-data"
anthropometric_data_service = AnthropometricDataService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateAnthropometricData(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a anthropometric data with a date")
    async def test_create_new_anthropometric_data_with_date(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "date": "2019-08-01",
                    "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                },
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert data["date"] == "2019-08-01"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a anthropometric data without a date")
    async def test_create_new_anthropometric_data_without_date(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                },
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert data["date"] == date.today().strftime("%Y-%m-%d")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a anthropometric data without required fields")
    async def test_create_anthropometric_data_without_required_field(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "user"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a anthropometric data without required authorization")
    async def test_create_anthropometric_data_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a anthropometric data without authorization")
    async def test_create_anthropometric_data_without_required_authorization(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                    },
                )
            ).status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/me/get")
class TestGetUserAnthropometricData(TestBaseE2E):
    route = f"/{CONTROLLER}/me/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get current user anthropometric data")
    async def test_get_current_user_anthropometric_data(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_common.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["user"]["id"] == str(user_common.user.id)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get current user anthropometric data without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get current user anthropometric data without anthropometric data")
    async def test_different_required_authentication(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_nutritionist)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAnthropometricDataByUserId(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get anthropometric data by user id")
    async def test_get_anthropometric_data_by_user_id(
        self, user_nutritionist: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                params={"search": f"user_id:{user_common.user.id}"},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["data"][0]["user"]["id"] == str(user_common.user.id)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get anthropometric data without required search field")
    async def test_get_anthropometric_data_without_user_id(
        self, user_nutritionist: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    self.route,
                    headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
                )
            ).status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get anthropometric data without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(self.route, params={"search": f"user_id:{user_common.user.id}"})
            ).status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get anthropometric data with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_admin"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    self.route,
                    params={"search": f"user_id:{user_common.user.id}"},
                    headers={"Authorization": f"Bearer {user.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<anthropometric_data_id>")
class TestGetAnthropometricDataId(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get anthropometric data id")
    async def test_get_anthropometric_data_by_user_id(
        self, user_nutritionist: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["id"] == "5bdf30ba-19cc-4954-8b98-c53aacd2793d"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get anthropometric data without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_no_authentication((self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get anthropometric data with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_admin"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(
            (self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d"), user
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<anthropometric_data_id>")
class TestUpdateAnthropometricData(TestBaseE2E):
    route = f"/{CONTROLLER}/update/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update anthropometric data")
    async def test_update_anthropometric_data(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                json={"height": 85},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["height"] == 85

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update anthropometric data without authentication")
    async def test_no_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_no_authentication((self.route + f"{user_common.user.id}"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update anthropometric data without required authentication")
    async def test_no_required_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_different_required_authentication(
            (self.route + f"{user_common.user.id}"), user_common
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/my-last-data/update")
class TestUpdateAnthropometricData(TestBaseE2E):
    route = f"/{CONTROLLER}/my-last-data/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update user anthropometric data")
    async def test_update_anthropometric_data(self, user_common: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route,
                json={"weight": 190},
                headers={"Authorization": f"Bearer {user_common.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/me/get",
                headers={"Authorization": f"Bearer {user_common.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["weight"] == 190

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update anthropometric data without authentication")
    async def test_no_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update anthropometric data without required authentication")
    async def test_no_required_authentication(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        await self.patch_different_required_authentication(self.route, user_nutritionist)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<anthropometric_data_id>")
class TestDeleteAnthropometricData(TestBaseE2E):
    route = f"/{CONTROLLER}/delete/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete anthropometric data")
    async def test_delete_user_anthropometric_data(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + "5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete the same anthropometric data twice")
    async def test_delete_same_user(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d",
                    headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete anthropometric data without authentication")
    async def test_no_authentication(self) -> None:
        await self.del_no_authentication((self.route + "5bdf30ba-19cc-4954-8b98-c53aacd2793d"))
