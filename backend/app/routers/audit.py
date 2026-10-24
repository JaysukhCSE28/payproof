"""POST /audit/{trip_id}, /audit/batch, and GET findings."""

import json
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from backend.app.db import get_connection
from backend.app.models import Finding
from backend.app.pipeline import run_audit

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("/batch")
def audit_batch() -> List[Dict[str, Any]]:
    """Audit all eligible ingested trips currently stored in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT trip_id FROM trips ORDER BY rowid ASC")
    rows = cursor.fetchall()
    conn.close()

    findings = []
    for r in rows:
        finding = run_audit(r["trip_id"])
        findings.append(finding.model_dump())

    return findings


@router.post("/{trip_id}")
def audit_single_trip(trip_id: str) -> Dict[str, Any]:
    """Execute deterministic audit on a single trip ID."""
    finding = run_audit(trip_id)
    return finding.model_dump()


@router.get("/findings")
def list_findings() -> List[Dict[str, Any]]:
    """List all audit findings from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM findings ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        d["breakdown"] = json.loads(d["breakdown_json"]) if d.get("breakdown_json") else None
        d["execution_log"] = json.loads(d["execution_log_json"]) if d.get("execution_log_json") else []
        results.append(d)
    return results


@router.get("/finding/{finding_id}")
def get_finding(finding_id: str) -> Dict[str, Any]:
    """Get single finding detail by finding_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM findings WHERE finding_id = ?", (finding_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Finding '{finding_id}' not found.")

    d = dict(row)
    d["breakdown"] = json.loads(d["breakdown_json"]) if d.get("breakdown_json") else None
    d["execution_log"] = json.loads(d["execution_log_json"]) if d.get("execution_log_json") else []
    return d


@router.get("/quarantine/list")
def list_quarantine() -> List[Dict[str, Any]]:
    """List all quarantined entries with reasons."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quarantine ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        item = dict(r)
        item["payload"] = json.loads(item["payload_json"]) if item.get("payload_json") else {}
        results.append(item)
    return results
