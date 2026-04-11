from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: int
    description: str
    completed: bool
    created_at: str
    completed_at: Optional[str] = None

    @staticmethod
    def now_iso() -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
