from pydantic import BaseModel, constr, Extra


class CreateAntecedentTypeDto(BaseModel):
    description: constr(max_length=255)

    class Config:
        extra = Extra.forbid
