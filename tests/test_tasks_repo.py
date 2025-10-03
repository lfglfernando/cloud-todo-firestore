import os
import pytest
from src.models.task import Task
from src.repo.tasks_repo import create_task, list_tasks, set_completed, delete_task

@pytest.mark.skipif(not os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and not os.getenv("FIRESTORE_EMULATOR_HOST"),
                    reason="Requiere credenciales o emulador")
def test_crud_flow(monkeypatch):
    user = "test-user"
    # Create
    tid = create_task(user, Task.new("Prueba", "desc", "2025-12-31"))
    assert tid

    # List
    tasks = list_tasks(user, status=None)
    assert any(t.id == tid for t in tasks)

    # Complete
    assert set_completed(user, tid, True) is True
    completed = list_tasks(user, status="completed")
    assert any(t.id == tid for t in completed)

    # Delete
    assert delete_task(user, tid) is True
