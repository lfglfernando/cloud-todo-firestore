from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: Optional[str]
    title: str
    description: str
    due_date: Optional[str]  # ISO YYYY-MM-DD
    completed: bool
    created_at: str
    updated_at: str

    @staticmethod
    def new(title: str, description: str = "", due_date: Optional[str] = None):
        now = datetime.utcnow().isoformat()
        return Task(
            id=None,
            title=title.strip(),
            description=description.strip(),
            due_date=due_date,
            completed=False,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self):
        d = asdict(self)
        return d
