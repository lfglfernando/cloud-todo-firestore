import os
from dotenv import load_dotenv
load_dotenv()

_db = None

def get_db():
    """
    Return a Firestore client.
    - If FIRESTORE_EMULATOR_HOST is set, use google-cloud-firestore Client directly (no creds).
    - Otherwise, use firebase_admin with service account JSON.
    """
    global _db
    if _db is not None:
        return _db

    emulator = os.getenv("FIRESTORE_EMULATOR_HOST")

    if emulator:
        from google.cloud import firestore as gc_fs
        project_id = os.getenv("FIREBASE_PROJECT_ID", "demo-no-project")
        _db = gc_fs.Client(project=project_id)
        return _db

    import firebase_admin
    from firebase_admin import credentials, firestore as admin_fs

    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not os.path.exists(creds_path):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is not set or file not found. "
            "Either set FIRESTORE_EMULATOR_HOST for local emulator or provide a valid service account JSON."
        )

    if not firebase_admin._apps:
        cred = credentials.Certificate(creds_path)
        firebase_admin.initialize_app(cred)

    _db = admin_fs.client()
    return _db
