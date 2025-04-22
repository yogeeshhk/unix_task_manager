from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.service import get_current_user
from src.db.database import get_db
from .constants import TaskStatus
from .schemas import TaskCreate, TaskResponse, PaginatedTaskResponse
from .service import (
    create_task, get_tasks, fork_task as fork_existing_task_logic,
    kill_task, get_task
)
from ..common.dependencies import PaginationParams

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=PaginatedTaskResponse)
def list_tasks(
        parent: int | None = Query(default=None),
        status: TaskStatus | None = Query(default=None),
        search: str | None = Query(default=None),
        sort_by: str = Query(default="created_at"),
        order: str = Query(default="desc", pattern="^(asc|desc)$"),
        pagination: PaginationParams = Depends(),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return get_tasks(
        db,
        current_user=current_user,
        parent_id=parent,
        status=status,
        search=search,
        limit=pagination.limit,
        offset=pagination.offset,
        sort_by=sort_by,
        order=order
    )


@router.get("/{task_id}", response_model=TaskResponse)
def retrieve_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_task(task_id, db, current_user)


@router.post("", response_model=TaskResponse, status_code=201)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task(db, task, current_user)


@router.post("/{task_id}/fork", response_model=TaskResponse, status_code=201)
def fork_existing_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return fork_existing_task_logic(task_id, db, current_user)


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return kill_task(task_id, db, current_user)
