from app.repositories.log_repository import LogRepository
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository, log_repository: LogRepository):
        self.task_repository = task_repository
        self.log_repository = log_repository

    def create(self, title: str, description: str = ""):
        task = self.task_repository.create(title=title, description=description)
        self.log_repository.create(action="create", target="task", target_id=task["id"], details=title)
        return task

    def list_all(self):
        return self.task_repository.list_all()

    def update(self, task_id: int, title: str, description: str = ""):
        task = self.task_repository.update(task_id=task_id, title=title, description=description)
        if task:
            self.log_repository.create(action="update", target="task", target_id=task_id, details=title)
        return task

    def complete(self, task_id: int):
        task = self.task_repository.mark_complete(task_id=task_id)
        if task:
            self.log_repository.create(action="complete", target="task", target_id=task_id)
        return task

    def delete(self, task_id: int):
        deleted = self.task_repository.delete(task_id)
        if deleted:
            self.log_repository.create(action="delete", target="task", target_id=task_id)
        return deleted
