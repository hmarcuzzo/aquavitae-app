import os
from typing import List

import pandas as pd

from config import ROOT_DIR
from src.core.types.exceptions_type import NotFoundException
from src.modules.domain.food.interfaces.food_category_interface import FoodCategoryInterface
from src.modules.domain.food.interfaces.food_interface import FoodInterface
from src.modules.infrastructure.database import get_db


def find_parent_id(
    system_types: pd.DataFrame,
    last_column_processed: pd.DataFrame,
    index: int,
):
    if last_column_processed.empty:
        return None

    parent = last_column_processed[index]
    if str(parent) == "nan":
        return None

    return system_types[system_types["description"] == parent]["id"].values[0]


async def import_default_category_foods(df: pd.DataFrame) -> pd.DataFrame:
    print("\nImporting default food categories...\n")
    food_category_interface = FoodCategoryInterface()

    system_types = pd.DataFrame()
    last_column_processed = pd.DataFrame()
    level = 0
    for column in list(df.columns.values):
        level += 1
        tmp_df = df[column].drop_duplicates()

        for index, row in tmp_df.items():
            if not isinstance(row, str):
                print(f"{index} Skipped: [{row}] (not a string)")
                continue

            with next(get_db()) as db_session:
                try:
                    result = await food_category_interface.find_one_category_by_description(
                        row, db_session
                    )
                except NotFoundException:
                    result = await food_category_interface.create_category(
                        description=row,
                        level=level,
                        parent=find_parent_id(
                            system_types,
                            last_column_processed,
                            index,
                        ),
                        db=db_session,
                    )
                    print(f"{index} Created: {row} ({result.id})")

                system_types = pd.concat(
                    [system_types, pd.DataFrame({"description": row, "id": result.id}, index=[0])],
                    ignore_index=True,
                )

        last_column_processed = df[column]

    print("\nImported or Loaded default food categories.\n")
    return system_types


def fix_row_values(row: pd.Series, food_columns: List[str]) -> pd.Series:
    for column in food_columns[1:-1]:
        if pd.isna(row[column]):
            row[column] = 0
    return row


async def import_default_foods(df: pd.DataFrame, system_types: pd.DataFrame):
    print("\nImporting default foods...\n")

    food_columns = [
        "Nome do alimento",
        "Proteínas\n[g]",
        "Lípidos\n[g]",
        "Hidratos de carbono\n[g]",
        "Energia\n[kcal]",
        "Potássio\n[mg]",
        "Fósforo\n[mg]",
        "Sódio\n[mg]",
        "Nível 3",
    ]

    df = df[food_columns]

    food_interface = FoodInterface()

    for index, row in df.iterrows():
        with next(get_db()) as db_session:
            try:
                await food_interface.find_one_food_by_description(
                    row["Nome do alimento"], db_session
                )
            except NotFoundException:
                row = fix_row_values(row, food_columns)
                food_category_id = (
                    system_types[system_types["description"] == row["Nível 3"]]["id"].values[0]
                    if not pd.isna(row["Nível 3"])
                    else None
                )

                if food_category_id is None:
                    print(f"{index} Skipped: {row['Nome do alimento']} (category not found)")
                    continue

                await food_interface.create_food(
                    description=row["Nome do alimento"],
                    proteins=row["Proteínas\n[g]"],
                    lipids=row["Lípidos\n[g]"],
                    carbohydrates=row["Hidratos de carbono\n[g]"],
                    energy_value=row["Energia\n[kcal]"],
                    potassium=row["Potássio\n[mg]"],
                    phosphorus=row["Fósforo\n[mg]"],
                    sodium=row["Sódio\n[mg]"],
                    food_category_id=food_category_id,
                    db=db_session,
                )
                print(f"{index} Created: {row['Nome do alimento']}")

    print("\nImported default foods.\n")


async def import_default_foods_and_category(
    file_name: str = "/src/static/doc/tca.xlsx", sheet_name: str = "insa_tca_v5_2021"
):
    file_name = input(f"File name [{file_name}]: ") or file_name
    sheet_name = input(f"Sheet name [{sheet_name}]: ") or sheet_name

    df = pd.read_excel(ROOT_DIR + os.path.join(file_name), sheet_name=sheet_name, header=1)
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df.rename(columns={c: c.replace(" \n", "\n") for c in df.columns}, inplace=True)
    system_types = await import_default_category_foods(df[["Nível 1", "Nível 2", "Nível 3"]])
    await import_default_foods(df, system_types)
