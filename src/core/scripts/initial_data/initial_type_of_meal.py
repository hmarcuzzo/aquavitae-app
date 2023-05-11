import os

import pandas as pd

from config import ROOT_DIR
from src.core.types.exceptions_type import NotFoundException
from src.modules.domain.meal.interfaces.type_of_meal_interface import TypeOfMealInterface
from src.modules.infrastructure.database import get_db


async def import_types_of_meal(df: pd.DataFrame) -> dict:
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


async def import_default_types_of_meal(
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
    system_types_of_meal = await import_types_of_meal(types_of_meal_df)

    return system_types_of_meal
