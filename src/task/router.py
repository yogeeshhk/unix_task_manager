from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from .schemas import TaskCreate, Task
from .service import create_task, get_tasks

router = APIRouter(
    prefix="",
    tags=["Tasks"]
)


@router.get("", response_model=list[Task])
def list_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def fork_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)
