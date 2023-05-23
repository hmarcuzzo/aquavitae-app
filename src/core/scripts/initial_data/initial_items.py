import os
from math import isnan
from typing import List
from uuid import UUID

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from config import ROOT_DIR
from src.core.types.exceptions_type import NotFoundException
from src.modules.domain.food.interfaces.food_interface import FoodInterface
from src.modules.domain.item.dto.item.list_has_food_dto import ListHasFoodDto
from src.modules.domain.item.interfaces.item_interface import ItemInterface
from src.modules.infrastructure.database import get_db


def get_item_can_eat_at(row: pd.Series, system_types_of_meal: dict) -> List[UUID]:
    row["meal_types"] = [
        item.strip() for x in row["meal_types"] if isinstance(x, str) for item in x.split(",")
    ]

    return [meal for can_eat_at in row["meal_types"] for meal in system_types_of_meal[can_eat_at]]


async def get_item_foods(
    item_description: str, row: pd.Series, food_interface: FoodInterface, db_session: Session
) -> List[ListHasFoodDto]:
    foods = []
    for i, food in enumerate(row["food_description"]):
        food = str(food).strip()
        try:
            food_dto = await food_interface.find_one_food_by_description(food, db_session)
            foods.append(
                ListHasFoodDto(
                    food=food_dto.id,
                    amount_grams=row["food_amount"][i],
                )
            )
        except NotFoundException:
            raise NotFoundException(f"Skipped: {item_description}, food '{food}' not found")

    return foods


async def item_exists(item_interface: ItemInterface, item_description: str, db: Session) -> bool:
    try:
        await item_interface.find_one_item_by_description(item_description, db)
    except NotFoundException:
        return False

    return True


async def import_items(df: pd.DataFrame, system_types_of_meal: dict):
    print("\nImporting default items...\n")
    item_interface = ItemInterface()
    food_interface = FoodInterface()

    for index, row in df.iterrows():
        if not isinstance(row, pd.Series):
            print(f"{index} Skipped: row {index} (not a string)")
            continue

        with next(get_db()) as db_session:
            if not (await item_exists(item_interface, str(index), db_session)):
                try:
                    item_foods = await get_item_foods(str(index), row, food_interface, db_session)
                    item_cat_eat_at = get_item_can_eat_at(row, system_types_of_meal)

                    await item_interface.create_item(
                        str(index), item_foods, item_cat_eat_at, db_session
                    )

                    print(f"Created: {str(index)}")
                except NotFoundException as e:
                    print(e.msg)
                    continue

    print("\nImported or Loaded default items.\n")


async def import_default_items(
    system_types_of_meal: dict,
    file_name: str = "/src/static/doc/items_system.xlsx",
    items_sheet_name: str = "AquaVitae",
):
    file_name = input(f"File name [{file_name}]: ") or file_name
    items_sheet_name = input(f"Items Sheet name [{items_sheet_name}]: ") or items_sheet_name

    items_df = (
        pd.read_excel(
            ROOT_DIR + os.path.join(file_name),
            sheet_name=items_sheet_name,
            header=0,
            engine="openpyxl",
        )
        .groupby("item_description")
        .agg(list)
    )
    await import_items(items_df, system_types_of_meal)
