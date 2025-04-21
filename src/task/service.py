from sqlalchemy.orm import Session

from .models import Task
from .schemas import TaskCreate


def get_tasks(db: Session):
    return db.query(Task).all()


def create_task(db: Session, task: TaskCreate):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
