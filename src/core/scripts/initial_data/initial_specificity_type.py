from src.core.constants.enum.specificity_type import SpecificityTypes
from src.core.types.exceptions_type import NotFoundException
from src.modules.domain.specificity.interfaces.specificity_type_interface import (
    SpecificityTypeInterface,
)
from src.modules.infrastructure.database import get_db


async def import_default_specificity_types() -> None:
    print("\nImporting default specificity types...\n")

    specificity_type_interface = SpecificityTypeInterface()

    for TYPE in SpecificityTypes:
        with next(get_db()) as db_session:
            try:
                await specificity_type_interface.find_one_specificity_type_by_description(
                    [TYPE.value], db_session
                )
            except NotFoundException:
                result = await specificity_type_interface.create_specificity_type(
                    description=TYPE.value,
                    db=db_session,
                )
                print(f"Created: {TYPE.value} ({result.id})")

    print("\nImported default specificity types.\n")
