from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.core.types.find_many_options_type import FindManyOptions
from src.main import app
from src.modules.domain.appointment.entities.appointment_has_appointment_goal_entity import (
    AppointmentHasAppointmentGoal,
)
from src.modules.domain.appointment.repositories.appointment_has_appointment_goal_repository import (
    AppointmentHasAppointmentGoalRepository,
)
from src.modules.domain.appointment.services.appointment_service import AppointmentService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "appointment"
appointment_service = AppointmentService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateAppointment(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an appointment")
    async def test_create_new_appointment(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "date": "2022-09-30",
                    "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                    "goals": ["dcf18594-13a1-4f8d-be14-8a6149a941e7"],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert data["status"] == "SCHEDULED"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a appointment without required fields")
    async def test_create_appointment_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "date"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a appointment without required authorization")
    async def test_create_appointment_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "date": "2022-09-30",
                        "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                        "goals": ["dcf18594-13a1-4f8d-be14-8a6149a941e7"],
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a appointment goal without authorization")
    async def test_create_appointment_goal_without_required_authorization(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "date": "2022-09-30",
                        "user": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                        "goals": ["dcf18594-13a1-4f8d-be14-8a6149a941e7"],
                    },
                )
            ).status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllAppointment(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get all appointments")
    async def test_get_all_appointment(self, user_nutritionist: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert "839f3db0-63e1-4e9d-af47-9000fc29a722" in [element["id"] for element in data["data"]]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.get(self.route)).status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    self.route,
                    headers={"Authorization": f"Bearer {user.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<appointment_id>")
class TestGetAppointmentById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get appointment by id")
    async def test_get_appointment_by_id(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["id"] == "839f3db0-63e1-4e9d-af47-9000fc29a722"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_no_authentication((self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(
            (self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722"), user
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<appointment_id>")
class TestUpdateAppointment(TestBaseE2E):
    route = f"/{CONTROLLER}/update/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update appointment removing goals")
    async def test_update_appointment_goal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722",
                json={"goals": None},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/839f3db0-63e1-4e9d-af47-9000fc29a722",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["appointment_has_goals"] == []

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update appointment without authentication")
    async def test_no_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_no_authentication(self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update appointment goal without required authentication")
    async def test_no_required_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_different_required_authentication(
            (self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722"), user_common
        )


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<appointment_id>")
class TestDeleteAppointment(TestBaseE2E):
    route = f"/{CONTROLLER}/delete/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete appointment")
    async def test_delete_appointment(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + "839f3db0-63e1-4e9d-af47-9000fc29a722",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Deleted appointment relationships must be deleted")
    async def test_delete_appointment_relationships(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        appointment_has_appointment_goal_repository = AppointmentHasAppointmentGoalRepository()
        appointment_has_appointment_goals = await appointment_has_appointment_goal_repository.find(
            {
                "where": AppointmentHasAppointmentGoal.appointment_id
                == "839f3db0-63e1-4e9d-af47-9000fc29a722"
            },
            self.db_test_utils.db,
        )

        assert appointment_has_appointment_goals == []

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete the same appointment twice")
    async def test_delete_same_appointment_goal(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete appointment without authentication")
    async def test_no_authentication(self) -> None:
        await self.del_no_authentication((self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete appointment without required authentication")
    async def test_no_required_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.del_different_required_authentication(
            (self.route + "839f3db0-63e1-4e9d-af47-9000fc29a722"), user_common
        )
