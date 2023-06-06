from typing import Optional

from pydantic import BaseModel, constr, Extra


class UpdateAntecedentTypeDto(BaseModel):
    description: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid
