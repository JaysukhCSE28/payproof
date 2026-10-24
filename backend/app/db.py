"""SQLite connection and schema initializer. DB file is created at runtime, not committed."""

import sqlite3
import os
from pathlib import Path
from backend.app.config import settings


def get_connection() -> sqlite3.Connection:
    """Return an open SQLite connection with WAL mode for concurrent access."""
    db_file = Path(settings.db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_file), check_same_thread=False, timeout=15)
    conn.row_factory = sqlite3.Row
    # WAL mode: allows concurrent reads+writes, fixing 'database is locked' under uvicorn
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = OFF;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create trips, findings, quarantine, clauses, rule_cards, and ledger tables."""
    cursor = conn.cursor()

    # Trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id TEXT PRIMARY KEY,
        employee_id TEXT,
        occurred_at TEXT,
        zone TEXT,
        city TEXT,
        vendor TEXT,
        vehicle_type TEXT,
        trip_type TEXT,
        distance_km TEXT,
        claimed_fare_inr TEXT,
        claimed_toll_inr TEXT,
        claimed_parking_inr TEXT,
        claimed_wait_inr TEXT,
        wait_minutes TEXT,
        is_night INTEGER DEFAULT 0,
        ocr_confidence REAL DEFAULT 1.0,
        ocr_text TEXT,
        notes TEXT,
        planted_error TEXT,
        raw_json TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # Policy Clauses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clauses (
        clause_id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        platform_vendor TEXT,
        zone TEXT,
        effective_from TEXT,
        effective_to TEXT,
        source_reference TEXT,
        tags TEXT
    );
    """)

    # Reviewed Rule Cards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rule_cards (
        rule_id TEXT PRIMARY KEY,
        version INTEGER NOT NULL,
        status TEXT NOT NULL,
        clause_id TEXT,
        zone TEXT,
        trip_type TEXT,
        effective_from TEXT,
        effective_to TEXT,
        formula_json TEXT NOT NULL
    );
    """)

    # Findings table (no FK on trip_id — integrity enforced by pipeline logic)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        finding_id TEXT PRIMARY KEY,
        trip_id TEXT NOT NULL,
        verdict TEXT NOT NULL,
        claimed_fare_inr TEXT,
        computed_fare_inr TEXT,
        verified_fare_inr TEXT,
        engine_delta_inr TEXT,
        tolerance_inr TEXT,
        rule_id TEXT,
        clause_id TEXT,
        evidence_packet_id TEXT,
        review_status TEXT DEFAULT 'pending',
        reason TEXT,
        breakdown_json TEXT,
        execution_log_json TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # Quarantine table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quarantine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id TEXT NOT NULL,
        reason TEXT NOT NULL,
        ocr_confidence REAL,
        payload_json TEXT NOT NULL,
        quarantined_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # Tamper-Evident Ledger table (no FK — chain integrity via SHA-256 hashing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ledger (
        event_id TEXT PRIMARY KEY,
        finding_id TEXT,
        payload_json TEXT NOT NULL,
        prev_hash TEXT NOT NULL,
        event_hash TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)

    conn.commit()
