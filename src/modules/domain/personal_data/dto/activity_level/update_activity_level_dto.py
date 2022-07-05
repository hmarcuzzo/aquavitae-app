from typing import Optional

from pydantic import BaseModel, conint, constr, Extra


class UpdateActivityLevelDto(BaseModel):
    description: Optional[constr(max_length=255)]
    factor: Optional[conint()]

    class Config:
        extra = Extra.forbid
