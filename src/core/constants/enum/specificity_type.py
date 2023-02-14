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
        return (
            SpecificityTypes.specificity_likes_consume()
            + SpecificityTypes.specificity_doesnt_like_consume()
        )

    @staticmethod
    def specificity_likes_consume() -> List[str]:
        return [
            SpecificityTypes.LIKE.value,
        ]

    @staticmethod
    def specificity_doesnt_like_consume() -> List[str]:
        return [
            SpecificityTypes.DON_T_LIKE.value,
        ]
