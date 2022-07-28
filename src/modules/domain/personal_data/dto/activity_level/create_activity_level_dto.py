from pydantic import BaseModel, conint, constr, Extra


class CreateActivityLevelDto(BaseModel):
    description: constr(max_length=255)
    factor: conint()

    class Config:
        extra = Extra.forbid
