from datetime import datetime

from sqlalchemy.orm import Session

from .constants import TaskStatus
from .models import Task
from .schemas import TaskCreate
from ..common.exceptions import NotFoundException, BadRequestException, UnprocessableEntityException


def get_tasks(
        db: Session,
        parent_id: int | None = None,
        status: TaskStatus | None = None,
        search: str | None = None,
        limit: int = 10,
        offset: int = 0,
        sort_by: str = "created_at",
        order: str = "desc"
) -> dict:
    query = db.query(Task)

    if parent_id is not None:
        query = query.filter(Task.parent_id == parent_id)

    if status is not None:
        query = query.filter(Task.status == status)

    if search:
        query = query.filter(Task.name.ilike(f"%{search}%"))

    VALID_SORT_FIELDS = {"created_at", "ended_at", "name", "status"}

    if sort_by not in VALID_SORT_FIELDS:
        raise BadRequestException(f"Invalid sort field '{sort_by}'. Must be one of {', '.join(VALID_SORT_FIELDS)}")
    else:
        sort_column = getattr(Task, sort_by)

    sort_direction = sort_column.desc() if order == "desc" else sort_column.asc()

    total = query.count()
    items = query.order_by(sort_direction).offset(offset).limit(limit).all()

    return {"total": total, "items": items}


def get_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException(f"Task with id {task_id} not found")
    return task


def create_task(db: Session, task: TaskCreate):
    if not task.name:
        raise UnprocessableEntityException("Task name is required")
    new_task = Task(
        name=task.name,
        status=TaskStatus.RUNNING
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def fork_task(parent_id: int, db: Session) -> Task:
    parent = db.query(Task).filter(Task.id == parent_id).first()

    if not parent:
        raise NotFoundException(f"Task with id {parent_id} not found")

    new_task = Task(
        name=parent.name,
        status=TaskStatus.RUNNING.value,
        created_at=datetime.utcnow(),
        started_at=datetime.utcnow(),
        parent_id=parent.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def kill_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException(f"Task with id {task_id} not found")

    if task.status != TaskStatus.RUNNING.value:
        raise BadRequestException("Only running tasks can be killed")

    task.status = TaskStatus.KILLED.value
    task.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
