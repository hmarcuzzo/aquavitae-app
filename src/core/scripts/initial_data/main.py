import asyncio

from src.core.scripts.initial_data.initial_food import import_default_foods_and_category
from src.core.scripts.initial_data.initial_specificity_type import import_default_specificity_types
from src.core.scripts.initial_data.initial_users import create_initial_users

if __name__ == "__main__":
    asyncio.run(create_initial_users())
    asyncio.run(import_default_foods_and_category())
    asyncio.run(import_default_specificity_types())
