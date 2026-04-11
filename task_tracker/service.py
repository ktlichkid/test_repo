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

    def _find_task_index(self, data: Dict[str, Any], task_id: int) -> int:
        tasks = data.get("tasks", [])
        for idx, t in enumerate(tasks):
            if t.get("id") == task_id:
                return idx
        return -1

    def complete(self, task_id: int) -> Task:
        data = self.repo.load()
        idx = self._find_task_index(data, task_id)
        if idx < 0:
            raise ValueError(f"No such task: {task_id}")
        t = data["tasks"][idx]
        if t.get("completed"):
            raise ValueError(f"Task already completed: {task_id}")
        t["completed"] = True
        t["completed_at"] = Task.now_iso()
        self.repo.save(data)
        return Task(**t)

    def delete(self, task_id: int) -> Task:
        data = self.repo.load()
        idx = self._find_task_index(data, task_id)
        if idx < 0:
            raise ValueError(f"No such task: {task_id}")
        removed = data["tasks"].pop(idx)
        self.repo.save(data)
        return Task(**removed)
