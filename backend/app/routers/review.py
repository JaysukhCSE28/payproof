"""POST /review/{finding_id}/approve, /reject."""

import json
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from backend.app.db import get_connection
from backend.app.ledger.chain import append_to_ledger

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/{finding_id}/approve")
def approve_finding(finding_id: str) -> Dict[str, Any]:
    """
    Explicit human review gate:
    Approves the finding and appends the canonicalized finding payload to the hash-chained ledger.
    Note: Does NOT autonomously submit grievances to external platforms.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM findings WHERE finding_id = ?", (finding_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Finding '{finding_id}' not found.")

    finding_dict = dict(row)
    if finding_dict.get("review_status") == "approved":
        return {
            "status": "already_approved",
            "message": f"Finding '{finding_id}' is already approved and recorded in the ledger."
        }

    finding_dict["breakdown"] = json.loads(finding_dict["breakdown_json"]) if finding_dict.get("breakdown_json") else None
    finding_dict["execution_log"] = json.loads(finding_dict["execution_log_json"]) if finding_dict.get("execution_log_json") else []

    # Commit to hash-chained ledger
    ledger_block = append_to_ledger(finding_id, finding_dict)

    return {
        "status": "approved",
        "message": f"Finding '{finding_id}' approved by human reviewer and committed to tamper-evident ledger.",
        "ledger_event": ledger_block
    }


@router.post("/{finding_id}/reject")
def reject_finding(finding_id: str, reason: str = "Discrepancy waived by worker") -> Dict[str, Any]:
    """Record human rejection without appending to the ledger."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM findings WHERE finding_id = ?", (finding_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Finding '{finding_id}' not found.")

    cursor.execute("""
    UPDATE findings SET review_status = 'rejected', reason = reason || ' [REJECTED: ' || ? || ']'
    WHERE finding_id = ?
    """, (reason, finding_id))
    conn.commit()
    conn.close()

    return {
        "status": "rejected",
        "message": f"Finding '{finding_id}' marked as rejected. No ledger entry created."
    }
