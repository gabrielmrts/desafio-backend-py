from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.task import TaskBase, TaskPatch, TaskRead, TaskCreate
from typing import List
from app.services.tasks import TaskService
from app.database.session import get_db
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get(
    "/", 
    tags=["tasks"],
    response_model=List[TaskRead]
)
@cache(expire=60)
def read_tasks(db: Session = Depends(get_db)):
    task_service = TaskService(db)
    tasks = task_service.get_all()
    return tasks

@router.post(
    "/", 
    tags=["tasks"],
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED
)
def create_task(task_create: TaskCreate, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.create(task_create)
    return task

@router.get(
    "/{task_id}", 
    tags=["tasks"],
    response_model=TaskRead
)
@cache(expire=120)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task_full(task_id: int, task_data: TaskBase, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.update_full(task_id, task_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskRead)
def update_task_partial(task_id: int, task_patch: TaskPatch, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.update_partial(task_id, task_patch)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete(
    "/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.delete(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
