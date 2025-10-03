import os
import typer
from rich import print
from tabulate import tabulate
from typing import Optional
from .models.task import Task
from .repo.tasks_repo import create_task, list_tasks, update_task, delete_task, set_completed

app = typer.Typer(help="To-Do on Firestore (Cloud DB)")

def _user():
    return os.getenv("DEFAULT_USER_ID", "demo-user")

@app.command()
def add(
    title: str = typer.Option(..., "--title", "-t", help="Task title (required)"),
    description: str = typer.Option("", "--desc", "-d", help="Description"),
    due_date: Optional[str] = typer.Option(None, "--due", help="YYYY-MM-DD")
):
    """Create a new task."""
    task = Task.new(title=title, description=description, due_date=due_date)
    task_id = create_task(_user(), task)
    print(f"[green]Created[/green] id={task_id} • {title}")

@app.command("list")
def list_cmd(
    status: Optional[str] = typer.Option(None, "--status", help="Filter: completed | pending")
):
    """List tasks."""
    tasks = list_tasks(_user(), status=status)
    rows = []
    for t in tasks:
        rows.append([t.id, "✔" if t.completed else "·", t.title, t.due_date or "", t.created_at.split("T")[0]])
    if rows:
        print(tabulate(rows, headers=["ID", "✓", "Title", "Due", "Created"], tablefmt="github"))
    else:
        print("[yellow]No tasks yet[/yellow]")

@app.command()
def done(task_id: str):
    """Mark a task as completed."""
    ok = set_completed(_user(), task_id, True)
    print("[green]OK[/green]" if ok else "[red]Not found[/red]")

@app.command()
def undone(task_id: str):
    """Unmark a task as completed."""
    ok = set_completed(_user(), task_id, False)
    print("[green]OK[/green]" if ok else "[red]Not found[/red]")

@app.command()
def update(
    task_id: str,
    title: Optional[str] = typer.Option(None, "--title", "-t"),
    description: Optional[str] = typer.Option(None, "--desc", "-d"),
    due_date: Optional[str] = typer.Option(None, "--due")
):
    """Update task fields."""
    fields = {}
    if title is not None: fields["title"] = title
    if description is not None: fields["description"] = description
    if due_date is not None: fields["due_date"] = due_date
    ok = update_task(_user(), task_id, fields)
    print("[green]Updated[/green]" if ok else "[red]Not found[/red]")

@app.command()
def delete(task_id: str):
    """Delete a task."""
    ok = delete_task(_user(), task_id)
    print("[green]Deleted[/green]" if ok else "[red]Not found[/red]")

if __name__ == "__main__":
    app()
