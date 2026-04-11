from typing import Dict, Any, List
from .domain import Task


class TaskService:
    def __init__(self, repo):
        self.repo = repo

    def add(self, description: str) -> Task:
        desc = description.strip()
        if not desc:
            raise ValueError("Description must not be empty")
        data = self.repo.load()
        task = Task(
            id=data["next_id"],
            description=desc,
            completed=False,
            created_at=Task.now_iso(),
            completed_at=None,
        )
        data["tasks"].append(task.__dict__)
        data["next_id"] += 1
        self.repo.save(data)
        return task

    def list(self) -> List[Task]:
        data = self.repo.load()
        tasks = [Task(**t) for t in data.get("tasks", [])]
        # Preserve creation order as stored
        return tasks
