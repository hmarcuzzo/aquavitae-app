from typing import Optional

from pydantic import BaseModel, constr, Extra


class UpdateAppointmentGoalDto(BaseModel):
    description: Optional[constr(min_length=1, max_length=1000)]

    class Config:
        extra = Extra.forbid
