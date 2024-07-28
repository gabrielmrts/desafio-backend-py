from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskPatch, TaskBase
from typing import Optional, List

class TaskService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> List[Task]:
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, task_create: TaskCreate) -> Task:
        task = Task(
            title=task_create.title,
            description=task_create.description
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_partial(self, task_id: int, task_patch: TaskPatch) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if task:
            task.completed = task_patch.completed
            self.db.commit()
            self.db.refresh(task)
        return task

    def update_full(self, task_id: int, task_data: TaskBase) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if task:
            task.title = task_data.title
            task.description = task_data.description
            task.completed = task_data.completed if task_data.completed is not None else task.completed
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return task
