from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.task import Task
from ..config.firebase import get_db

def _col(user_id: str):
    db = get_db()
    return db.collection("users").document(user_id).collection("tasks")

def create_task(user_id: str, task: Task) -> str:
    ref = _col(user_id).document()
    task.id = ref.id
    ref.set(task.to_dict())
    return ref.id

def list_tasks(user_id: str, status: Optional[str] = None) -> List[Task]:
    q = _col(user_id)
    if status == "completed":
        q = q.where("completed", "==", True)
    elif status == "pending":
        q = q.where("completed", "==", False)

    docs = q.order_by("created_at").stream()
    tasks: List[Task] = []
    for d in docs:
        data = d.to_dict()
        data["id"] = d.id
        tasks.append(Task(**data))
    return tasks

def get_task(user_id: str, task_id: str) -> Optional[Task]:
    snap = _col(user_id).document(task_id).get()
    if not snap.exists:
        return None
    data = snap.to_dict()
    data["id"] = snap.id
    return Task(**data)

def update_task(user_id: str, task_id: str, fields: Dict[str, Any]) -> bool:
    ref = _col(user_id).document(task_id)
    if not ref.get().exists:
        return False
    fields["updated_at"] = datetime.utcnow().isoformat()
    ref.update(fields)
    return True

def delete_task(user_id: str, task_id: str) -> bool:
    ref = _col(user_id).document(task_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True

def set_completed(user_id: str, task_id: str, value: bool) -> bool:
    return update_task(user_id, task_id, {"completed": value})
