"""End-to-end audit pipeline orchestrator."""

import json
import uuid
from decimal import Decimal
from typing import Dict, Any, Optional
from backend.app.db import get_connection
from backend.app.models import Finding, Verdict
from backend.app.language.abstain import should_abstain_from_trip
from backend.app.evidence.quarantine import quarantine_trip
from backend.app.retrieval.retriever import PolicyRetriever
from backend.app.calc.engine import compute_fare, round_inr
from backend.app.calc.verifier import compute_fare_paise
from backend.app.calc.compare import compare_amounts
from backend.app.ledger.packet import build_evidence_packet
from backend.app.config import settings

_retriever = PolicyRetriever()


def run_audit(trip_id: str, trip_data: Optional[Dict[str, Any]] = None) -> Finding:
    """
    Orchestrate full audit pipeline:
    1. Ingestion / Fetch
    2. Input & Confidence Gates (Abstain/Quarantine)
    3. Policy Retrieval & Rule Resolution
    4. Deterministic Dual-Calculation
    5. Tolerance Verification
    6. Finding & Evidence Packet Assembly
    """
    execution_log = []
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Fetch trip if not passed
    if trip_data is None:
        cursor.execute("SELECT * FROM trips WHERE trip_id = ?", (trip_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return quarantine_trip(trip_id, f"Trip record '{trip_id}' not found in database.", {})
        trip_data = dict(row)

    execution_log.append(f"01 INGEST: Loaded Trip {trip_id}")

    # Step 2: Abstention & Confidence Gate
    should_abstain, abstain_reason = should_abstain_from_trip(trip_data)
    if should_abstain:
        conn.close()
        finding = quarantine_trip(trip_id, abstain_reason, trip_data, trip_data.get("ocr_confidence"))
        return finding

    execution_log.append(
        f"02 EXTRACT: Vendor={trip_data.get('vendor')}, Zone={trip_data.get('zone')}, "
        f"Dist={trip_data.get('distance_km')}km, Claimed=₹{trip_data.get('claimed_fare_inr')}, "
        f"OCR Conf={float(trip_data.get('ocr_confidence', 1.0))*100:.1f}%"
    )

    # Step 3: Policy Retrieval & Rule Resolution
    clause, rule_card, ret_msg = _retriever.retrieve(trip_data)
    if not rule_card:
        conn.close()
        finding = quarantine_trip(trip_id, ret_msg, trip_data, trip_data.get("ocr_confidence"))
        return finding

    execution_log.append(
        f"03 RETRIEVE: Matched Clause {clause.get('clause_id')} -> "
        f"Rule Card {rule_card.get('rule_id')} (v{rule_card.get('version')})"
    )

    # Step 4: Primary Decimal Calculation
    try:
        computed_decimal, breakdown = compute_fare(trip_data, rule_card)
        execution_log.append(f"04 COMPUTE: Decimal Engine computed ₹{computed_decimal:.2f}")
    except Exception as e:
        conn.close()
        return quarantine_trip(trip_id, f"Calculation exception: {str(e)}", trip_data)

    # Step 5: Independent Integer-Paise Verification
    try:
        verified_paise = compute_fare_paise(trip_data, rule_card)
        execution_log.append(f"05 VERIFY: Integer-Paise Engine verified {verified_paise} paise (₹{verified_paise/100:.2f})")
    except Exception as e:
        conn.close()
        return quarantine_trip(trip_id, f"Paise verification exception: {str(e)}", trip_data)

    # Step 6: Tolerance Logic & Verdict Classification
    claimed_decimal = round_inr(Decimal(str(trip_data.get("claimed_fare_inr", "0.00"))))
    verdict, difference, compare_reason = compare_amounts(claimed_decimal, computed_decimal, verified_paise)

    if verdict == "CANNOT_DETERMINE":
        conn.close()
        return quarantine_trip(trip_id, compare_reason, trip_data)

    execution_log.append(f"06 COMPARE: Delta=₹{difference:+.2f} vs ₹{settings.amount_tolerance_inr} tolerance -> {verdict}")
    execution_log.append(f"07 VERDICT: {verdict} - {compare_reason}")

    # Step 7: Build Evidence Packet
    finding_id = f"FIND-{uuid.uuid4().hex[:8].upper()}"
    evidence_packet = build_evidence_packet(
        trip=trip_data,
        finding_id=finding_id,
        rule_card=rule_card,
        clause=clause,
        breakdown=breakdown,
        execution_log=execution_log
    )

    finding = Finding(
        finding_id=finding_id,
        trip_id=trip_id,
        verdict=verdict,
        claimed_fare_inr=str(claimed_decimal),
        computed_fare_inr=str(computed_decimal),
        verified_fare_inr=f"{verified_paise / 100:.2f}",
        engine_delta_inr=str(difference),
        tolerance_inr=settings.amount_tolerance_inr,
        rule_id=rule_card.get("rule_id"),
        clause_id=clause.get("clause_id"),
        evidence_packet_id=evidence_packet["evidence_packet_id"],
        review_status="pending",
        reason=compare_reason,
        breakdown=breakdown,
        execution_log=execution_log
    )

    # Save to findings table
    cursor.execute("""
    INSERT OR REPLACE INTO findings (
        finding_id, trip_id, verdict, claimed_fare_inr, computed_fare_inr, verified_fare_inr,
        engine_delta_inr, tolerance_inr, rule_id, clause_id, evidence_packet_id, review_status,
        reason, breakdown_json, execution_log_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        finding.finding_id, finding.trip_id, finding.verdict, finding.claimed_fare_inr,
        finding.computed_fare_inr, finding.verified_fare_inr, finding.engine_delta_inr,
        finding.tolerance_inr, finding.rule_id, finding.clause_id, finding.evidence_packet_id,
        finding.review_status, finding.reason, json.dumps(breakdown), json.dumps(execution_log)
    ))
    conn.commit()
    conn.close()

    return finding
