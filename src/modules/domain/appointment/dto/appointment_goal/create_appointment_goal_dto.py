from pydantic import BaseModel, constr


class CreateAppointmentGoalDto(BaseModel):
    description: constr(max_length=1000)

    class Config:
        orm_mode = True
