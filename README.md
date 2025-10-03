# Cloud To-Do (Python + Firebase/Firestore)

A simple CLI app to demonstrate a **cloud database** with full **CRUD** in Firestore using Python.

## Goals
- Use Firestore with at least one collection.
- Create, read, update, and delete data.
- (Optional) Add user authentication later (a demo user is provided).

## Tech Stack
- Python 3.10+
- `firebase-admin`
- Firestore (`users/{userId}/tasks`)
- Typer (CLI), Rich/Tabulate (pretty terminal output)
- Pytest (tests)

---

## Installation (macOS / Linux)

Run these commands from the **project root** (where `requirements.txt` is located):

```bash
# 1) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Upgrade packaging tools and install dependencies
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt

# 3) Initialize Python packages if needed (prevents "No module named src")
touch src/__init__.py src/config/__init__.py src/models/__init__.py src/repo/__init__.py

# 4) Create your .env from the example
cp .env.example .env  # edit GOOGLE_APPLICATION_CREDENTIALS only if you will use the Cloud option
