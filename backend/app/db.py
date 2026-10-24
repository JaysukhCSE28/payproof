"""SQLite connection and schema initializer. DB file is created at runtime, not committed."""

import sqlite3

from backend.app.config import settings


def get_connection() -> sqlite3.Connection:
    # TODO: enable foreign keys and row factory
    return sqlite3.connect(settings.db_path)


def init_schema(conn: sqlite3.Connection) -> None:
    # TODO: create trips, findings, quarantine, and ledger tables
    raise NotImplementedError("init_schema")
