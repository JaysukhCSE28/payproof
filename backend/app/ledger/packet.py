"""JSON evidence packet builder."""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def build_evidence_packet(
    trip: Dict[str, Any],
    finding_id: str,
    rule_card: Optional[Dict[str, Any]],
    clause: Optional[Dict[str, Any]],
    breakdown: Optional[Dict[str, Any]],
    execution_log: list
) -> Dict[str, Any]:
    """Create a structured, immutable evidence packet for review and ledger commit."""
    packet_id = f"EVID-{uuid.uuid4().hex[:12].upper()}"
    return {
        "evidence_packet_id": packet_id,
        "finding_id": finding_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trip_snapshot": trip,
        "rule_card_snapshot": {
            "rule_id": rule_card.get("rule_id") if rule_card else None,
            "version": rule_card.get("version") if rule_card else None,
            "formula": rule_card.get("formula") if rule_card else None
        } if rule_card else None,
        "clause_snapshot": {
            "clause_id": clause.get("clause_id") if clause else None,
            "source_reference": clause.get("source_reference") if clause else None,
            "text": clause.get("text") if clause else None
        } if clause else None,
        "arithmetic_breakdown": breakdown,
        "execution_log": execution_log,
        "integrity": {
            "auditor": "PayProof Deterministic Engine v1.0",
            "is_human_reviewed": False
        }
    }
