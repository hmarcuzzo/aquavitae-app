import asyncio

from src.core.scripts.initial_data.initial_food import import_default_foods_and_category
from src.core.scripts.initial_data.initial_items import import_default_items
from src.core.scripts.initial_data.initial_specificity_type import import_default_specificity_types
from src.core.scripts.initial_data.initial_type_of_meal import (
    import_default_types_of_meal,
)
from src.core.scripts.initial_data.initial_users import create_initial_users

if __name__ == "__main__":
    asyncio.run(create_initial_users())
    asyncio.run(import_default_foods_and_category())
    system_types_of_meal = asyncio.run(import_default_types_of_meal())
    asyncio.run(import_default_specificity_types())
    asyncio.run(import_default_items(system_types_of_meal))
