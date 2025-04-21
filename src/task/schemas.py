from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    status: str = "running"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
