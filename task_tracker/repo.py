import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_STORE = Path(".tasks.json")


class TaskRepository:
    def __init__(self, path: Path = DEFAULT_STORE):
        self.path = path

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {"next_id": 1, "tasks": []}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if "next_id" not in data:
            data["next_id"] = 1
        if "tasks" not in data:
            data["tasks"] = []
        return data

    def save(self, data: Dict[str, Any]) -> None:
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(self.path)
