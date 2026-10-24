"""Quarantine handler for low-confidence or unparseable inputs."""

import json
from typing import Dict, Any, Optional
import sqlite3
from backend.app.models import Finding
from backend.app.db import get_connection


def quarantine_trip(
    trip_id: str,
    reason: str,
    payload: Dict[str, Any],
    ocr_confidence: Optional[float] = None
) -> Finding:
    """Insert into quarantine table and construct CANNOT_DETERMINE finding."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO quarantine (trip_id, reason, ocr_confidence, payload_json)
    VALUES (?, ?, ?, ?)
    """, (trip_id, reason, ocr_confidence, json.dumps(payload, default=str)))
    conn.commit()
    conn.close()

    finding = Finding(
        finding_id=f"FINDING-Q-{trip_id}",
        trip_id=trip_id,
        verdict="CANNOT_DETERMINE",
        claimed_fare_inr=str(payload.get("claimed_fare_inr", "0.00")),
        computed_fare_inr=None,
        verified_fare_inr=None,
        engine_delta_inr=None,
        tolerance_inr="1.00",
        rule_id=None,
        clause_id=None,
        review_status="pending",
        reason=f"QUARANTINED: {reason}",
        breakdown={"quarantine": True, "reason": reason},
        execution_log=[
            f"INIT: Trip {trip_id}",
            f"ABSTAIN: Quarantined - {reason}",
            "VERDICT: CANNOT_DETERMINE"
        ]
    )
    return finding
