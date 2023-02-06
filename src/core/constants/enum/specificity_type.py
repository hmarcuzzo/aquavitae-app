from enum import Enum
from typing import List


class SpecificityTypes(Enum):
    ALLERGIC = "ALLERGIC"
    INTOLERANT = "INTOLERANT"
    SENSITIVE = "SENSITIVE"
    LIKE = "LIKE"
    DON_T_LIKE = "DON'T LIKE"

    @staticmethod
    def specificity_forbidden_consume() -> List[str]:
        return [
            SpecificityTypes.ALLERGIC.value,
            SpecificityTypes.INTOLERANT.value,
            SpecificityTypes.SENSITIVE.value,
        ]

    @staticmethod
    def specificity_preferences_consumption() -> List[str]:
        return [
            SpecificityTypes.LIKE.value,
            SpecificityTypes.DON_T_LIKE.value,
        ]
