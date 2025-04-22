from datetime import datetime
from sqlalchemy.orm import Session

from .constants import TaskStatus
from .models import Task
from .schemas import TaskCreate
from ..auth.models import User
from ..common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    BadRequestException,
    UnprocessableEntityException,
)
from ..common.logger import get_logger

logger = get_logger(__name__)


def get_tasks(
    db: Session,
    current_user: User,
    parent_id: int | None = None,
    status: TaskStatus | None = None,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    order: str = "desc"
) -> dict:
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if parent_id is not None:
        query = query.filter(Task.parent_id == parent_id)
    if status is not None:
        query = query.filter(Task.status == status)
    if search:
        query = query.filter(Task.name.ilike(f"%{search}%"))

    VALID_SORT_FIELDS = {"created_at", "ended_at", "name", "status"}
    if sort_by not in VALID_SORT_FIELDS:
        logger.warning(f"Invalid sort field: {sort_by}")
        raise BadRequestException(
            f"Invalid sort field '{sort_by}'. Must be one of {', '.join(VALID_SORT_FIELDS)}"
        )

    sort_column = getattr(Task, sort_by)
    sort_direction = sort_column.desc() if order == "desc" else sort_column.asc()

    total = query.count()
    items = query.order_by(sort_direction).offset(offset).limit(limit).all()

    logger.info(f"Returning {len(items)} tasks out of {total}")
    return {"total": total, "items": items}


def get_task(task_id: int, db: Session, current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise NotFoundException(f"Task with id {task_id} not found")

    if task.user_id != current_user.id:
        logger.warning(f"Unauthorized access by '{current_user.username}' on task {task_id}")
        raise UnauthorizedException("You do not have permission to view this task.")

    logger.info(f"Task {task_id} returned to user {current_user.username}")
    return task


def create_task(db: Session, task: TaskCreate, current_user: User):
    if not task.name:
        logger.error("Task name is required but was not provided")
        raise UnprocessableEntityException("Task name is required")

    new_task = Task(
        name=task.name,
        status=TaskStatus.RUNNING,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info(f"Task created with id: {new_task.id} by user {current_user.username}")
    return new_task


def fork_task(parent_id: int, db: Session, current_user: User) -> Task:
    parent = db.query(Task).filter(Task.id == parent_id).first()

    if not parent:
        raise NotFoundException(f"Task with id {parent_id} not found")

    if parent.user_id != current_user.id:
        logger.warning(f"User '{current_user.username}' unauthorized to fork task {parent_id}")
        raise UnauthorizedException("You do not have permission to fork this task.")

    new_task = Task(
        name=parent.name,
        status=TaskStatus.RUNNING.value,
        created_at=datetime.utcnow(),
        started_at=datetime.utcnow(),
        parent_id=parent.id,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info(f"User '{current_user.username}' forked task {parent.id} to new task {new_task.id}")
    return new_task


def kill_task(task_id: int, db: Session, current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise NotFoundException(f"Task with id {task_id} not found")

    if task.user_id != current_user.id:
        logger.warning(f"User '{current_user.username}' unauthorized to kill task {task_id}")
        raise UnauthorizedException("You do not have permission to delete this task.")

    if task.status != TaskStatus.RUNNING.value:
        raise BadRequestException("Only running tasks can be killed")

    task.status = TaskStatus.KILLED.value
    task.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    logger.info(f"User '{current_user.username}' killed task {task_id}")
    return task
