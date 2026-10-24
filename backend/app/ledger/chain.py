"""SHA-256 append and chain verifier."""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from backend.app.db import get_connection
from backend.app.ledger.canonical import canonicalize


def compute_event_hash(prev_hash: str, canonical_payload: str, timestamp: str) -> str:
    """Deterministic SHA-256 hash chaining function."""
    raw = f"{prev_hash}|{canonical_payload}|{timestamp}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def append_to_ledger(finding_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Append an explicitly approved finding payload to the hash-chained ledger."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch previous hash
    cursor.execute("SELECT event_hash FROM ledger ORDER BY rowid DESC LIMIT 1")
    row = cursor.fetchone()
    prev_hash = row["event_hash"] if row else "0" * 64

    event_id = f"EVT-{uuid.uuid4().hex[:12].upper()}"
    timestamp = datetime.now(timezone.utc).isoformat()
    canonical_payload_str = canonicalize(payload)
    event_hash = compute_event_hash(prev_hash, canonical_payload_str, timestamp)

    cursor.execute("""
    INSERT INTO ledger (event_id, finding_id, payload_json, prev_hash, event_hash, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (event_id, finding_id, canonical_payload_str, prev_hash, event_hash, timestamp))

    # Mark finding as approved in findings table if present
    cursor.execute("UPDATE findings SET review_status = 'approved' WHERE finding_id = ?", (finding_id,))

    conn.commit()
    conn.close()

    return {
        "event_id": event_id,
        "finding_id": finding_id,
        "prev_hash": prev_hash,
        "event_hash": event_hash,
        "timestamp": timestamp,
        "payload": payload
    }


def list_ledger_events() -> List[Dict[str, Any]]:
    """Retrieve all ledger events ordered chronologically."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, finding_id, payload_json, prev_hash, event_hash, timestamp FROM ledger ORDER BY rowid ASC")
    rows = cursor.fetchall()
    conn.close()

    events = []
    for r in rows:
        events.append({
            "event_id": r["event_id"],
            "finding_id": r["finding_id"],
            "payload": json.loads(r["payload_json"]),
            "prev_hash": r["prev_hash"],
            "event_hash": r["event_hash"],
            "timestamp": r["timestamp"]
        })
    return events


def verify_chain() -> Dict[str, Any]:
    """Verify integrity of all hash links in the ledger."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, payload_json, prev_hash, event_hash, timestamp FROM ledger ORDER BY rowid ASC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"valid": True, "total_blocks": 0, "message": "Ledger is empty."}

    expected_prev = "0" * 64
    for idx, r in enumerate(rows, 1):
        if r["prev_hash"] != expected_prev:
            return {
                "valid": False,
                "broken_at_event_id": r["event_id"],
                "block_number": idx,
                "reason": f"Previous hash mismatch at event {r['event_id']}. Expected {expected_prev}, got {r['prev_hash']}."
            }

        recomputed = compute_event_hash(r["prev_hash"], r["payload_json"], r["timestamp"])
        if recomputed != r["event_hash"]:
            return {
                "valid": False,
                "broken_at_event_id": r["event_id"],
                "block_number": idx,
                "reason": f"Tamper detected! Signature invalid at event {r['event_id']}. Expected {recomputed}, stored {r['event_hash']}."
            }
        expected_prev = r["event_hash"]

    return {
        "valid": True,
        "total_blocks": len(rows),
        "message": f"All {len(rows)} ledger blocks verified intact."
    }


def tamper_ledger_entry(event_id: str, new_payload: Dict[str, Any]) -> bool:
    """Deliberately modify a ledger entry without updating the hash to demonstrate tamper detection."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ledger SET payload_json = ? WHERE event_id = ?", (canonicalize(new_payload), event_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0
