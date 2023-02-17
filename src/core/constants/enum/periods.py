from enum import Enum


class Periods(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BY_MEAL = "BY_MEAL"

    @property
    def days(self):
        if self == Periods.DAILY:
            return 1
        elif self == Periods.WEEKLY:
            return 7
        elif self == Periods.BY_MEAL:
            return None
