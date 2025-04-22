from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.common.pagination import PaginatedResponse
from src.task.constants import TaskStatus


class TaskCreate(BaseModel):
    name: str


class TaskResponse(BaseModel):
    id: int
    name: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedTaskResponse(PaginatedResponse[TaskResponse]):
    pass
