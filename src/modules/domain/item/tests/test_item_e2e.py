from typing import Optional

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.services.item_service import ItemService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "item"
item_service = ItemService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateItem(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an item")
    async def test_create_item_one_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Item 1",
                    "foods": [
                        {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"}
                    ],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "foods"]]
        assert len(data["foods"]) == 1
        assert data["foods"][0] == "950d760f-ba5c-44ca-b4ec-313510e59beb"

        new_item = self.db_test_utils.db.query(Item).where(Item.id == data["id"]).first()
        assert len(new_item.foods) == 1
        assert new_item.foods[0].amount_grams == 200

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an item with multiples foods")
    async def test_create_item_multiples_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Item Many Foods",
                    "foods": [
                        {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"},
                        {"amount_grams": 150, "food": "e3ff57d6-eb77-48de-bb49-ff9201d95926"},
                    ],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "foods"]]
        assert len(data["foods"]) == 2
        assert (
            "950d760f-ba5c-44ca-b4ec-313510e59beb" and "e3ff57d6-eb77-48de-bb49-ff9201d95926"
        ) in data["foods"]

        new_item = self.db_test_utils.db.query(Item).where(Item.id == data["id"]).first()
        assert len(new_item.foods) == 2

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a item with deleted food")
    async def test_create_item_with_deleted_food(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Item Deleted Food",
                        "foods": [
                            {"amount_grams": 200, "food": "0e8dbb8d-bf41-484d-90af-7c44fc4cb6fc"}
                        ],
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a item without required fields")
    async def test_create_item_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={"description": "Item Deleted Food"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "foods"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food without required authorization")
    async def test_create_item_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Item User",
                        "foods": [
                            {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"}
                        ],
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN
