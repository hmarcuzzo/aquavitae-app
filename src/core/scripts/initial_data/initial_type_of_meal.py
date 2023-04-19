import os

import pandas as pd

from config import ROOT_DIR
from src.core.types.exceptions_type import NotFoundException
from src.modules.domain.meal.interfaces.type_of_meal_interface import TypeOfMealInterface
from src.modules.infrastructure.database import get_db


async def import_default_types_of_meal(df: pd.DataFrame) -> dict:
    print("\nImporting default types of meal...\n")
    type_of_meal_interface = TypeOfMealInterface()

    system_types_of_meal = {}

    for index, row in df.iterrows():
        if not isinstance(row, pd.Series):
            print(f"{index} Skipped: row {index} (not a string)")
            continue

        with next(get_db()) as db_session:
            try:
                result = await type_of_meal_interface.find_one_type_of_meal_by_description(
                    row["description"], db_session
                )
            except NotFoundException:
                result = await type_of_meal_interface.create_type_of_meal(
                    description=row["description"],
                    calories=float(row["calories percentage"]),
                    lipids=float(row["lipids percentage"]),
                    proteins=float(row["proteins percentage"]),
                    carbohydrates=float(row["carbohydrates percentage"]),
                    db=db_session,
                )
                print(f"{index} Created: {row['description']} ({result.id})")

            system_types_of_meal[row["abbreviation"]] = [result.id]

    print("\nImported or Loaded default types of meal.\n")

    return system_types_of_meal


# async def import_default_can_eat_at(df: pd.DataFrame, system_meal_types: dict):
#     print("\nImporting default can eat at...\n")
#     food_category_interface = FoodCategoryInterface()
#     food_cat_eat_at_interface = FoodCanEatAtInterface()
#
#     df.drop_duplicates(subset=["description", "can eat at"], inplace=True)
#
#     for index, row in df.iterrows():
#         with next(get_db()) as db_session:
#             food_category = await food_category_interface.find_one_category_by_description(
#                 row["description"], db_session
#             )
#
#             foods = pd.DataFrame.from_records(
#                 [
#                     food.__dict__
#                     for food in food_category_interface.get_all_foods_from_category(food_category)
#                 ]
#             ).drop_duplicates(subset=["id"])
#
#             for food in foods.itertuples():
#                 for meal_type_id in system_meal_types[row["can eat at"]]:
#                     try:
#                         await food_cat_eat_at_interface.find_one_can_eat_at(
#                             meal_type_id, food.id, db_session
#                         )
#                     except NotFoundException:
#                         await food_cat_eat_at_interface.create_food_can_eat_at(
#                             meal_type_id, food.id, db_session
#                         )
#                         print(f"{index} Created: {food.description} ({food.id})")
#
#     print("\nImported default can eat eat.\n")


async def import_default_types_of_meal_and_can_eat_at(
    file_name: str = "/src/static/doc/type_of_meal.xlsx",
    type_of_meal_sheet_name: str = "type_of_meal",
) -> dict:
    file_name = input(f"File name [{file_name}]: ") or file_name
    type_of_meal_sheet_name = (
        input(f"Type of Meal Sheet name [{type_of_meal_sheet_name}]: ") or type_of_meal_sheet_name
    )

    types_of_meal_df = pd.read_excel(
        ROOT_DIR + os.path.join(file_name), sheet_name=type_of_meal_sheet_name, header=0
    )
    system_types_of_meal = await import_default_types_of_meal(types_of_meal_df)

    # await import_default_can_eat_at(can_eat_at_df, system_types_of_meal)
    return system_types_of_meal
