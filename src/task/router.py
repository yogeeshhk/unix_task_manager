from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.db.database import get_db
from .constants import TaskStatus
from .schemas import TaskCreate, TaskResponse, PaginatedTaskResponse
from .service import create_task, get_tasks, fork_task as fork_existing_task_logic, kill_task, get_task
from ..common.dependencies import PaginationParams
from ..common.exceptions import NotFoundException, UnprocessableEntityException

router = APIRouter(
    tags=["Tasks"]
)


@router.get("", response_model=PaginatedTaskResponse)
def list_tasks(
        parent: int | None = Query(default=None),
        status: TaskStatus | None = Query(default=None),
        search: str | None = Query(default=None),
        sort_by: str = Query(default="created_at"),
        order: str = Query(default="desc", pattern="^(asc|desc)$"),
        pagination: PaginationParams = Depends(),
        db: Session = Depends(get_db)
):
    return get_tasks(
        db,
        parent_id=parent,
        status=status,
        search=search,
        limit=pagination.limit,
        offset=pagination.offset,
        sort_by=sort_by,
        order=order
    )


@router.get("/{task_id}", response_model=TaskResponse)
def retrieve_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return get_task(task_id, db)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        return create_task(db, task)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating task: {str(e)}"
        )


@router.post("/{task_id}/fork", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def fork_existing_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return fork_existing_task_logic(task_id, db)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnprocessableEntityException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while forking task: {str(e)}"
        )


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return kill_task(task_id, db)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while deleting task: {str(e)}"
        )
