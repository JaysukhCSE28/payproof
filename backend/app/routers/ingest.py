"""POST /ingest/trips, /screenshot, /policy and GET /ingest/trips."""

import json
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.db import get_connection
from backend.app.evidence.csv_loader import parse_csv_content
from backend.app.evidence.normalizer import normalize_trip_dict
from backend.app.evidence.ocr import extract_text_from_image
from backend.app.language.extractor import extract_trip_fields
from backend.app.retrieval.clause_parser import parse_raw_policy_text

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/trips")
async def ingest_trips(file: UploadFile = File(None)) -> Dict[str, Any]:
    """Accept CSV upload, validate against trip schema, persist to SQLite."""
    if not file:
        raise HTTPException(status_code=400, detail="CSV file must be provided.")
    
    contents = await file.read()
    try:
        text = contents.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode CSV: {str(e)}")

    trips = parse_csv_content(text)
    if not trips:
        raise HTTPException(status_code=400, detail="No valid trip rows found in CSV.")

    conn = get_connection()
    cursor = conn.cursor()
    saved_count = 0
    for t in trips:
        cursor.execute("""
        INSERT OR REPLACE INTO trips (
            trip_id, employee_id, occurred_at, zone, city, vendor, vehicle_type, trip_type,
            distance_km, claimed_fare_inr, claimed_toll_inr, claimed_parking_inr, claimed_wait_inr,
            wait_minutes, is_night, ocr_confidence, ocr_text, notes, planted_error, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["trip_id"], t["employee_id"], t["occurred_at"], t["zone"], t["city"],
            t["vendor"], t["vehicle_type"], t["trip_type"], t["distance_km"],
            t["claimed_fare_inr"], t["claimed_toll_inr"], t["claimed_parking_inr"],
            t["claimed_wait_inr"], t["wait_minutes"], 1 if t["is_night"] else 0,
            t["ocr_confidence"], t["ocr_text"], t["notes"], t["planted_error"],
            json.dumps(t)
        ))
        saved_count += 1

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "trips_ingested": saved_count,
        "sample_trip_ids": [t["trip_id"] for t in trips[:5]]
    }


@router.get("/trips")
def list_trips() -> List[Dict[str, Any]]:
    """List all ingested trips from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/screenshot")
async def ingest_screenshot(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Run OCR check and structured extraction on receipt screenshot."""
    contents = await file.read()
    ocr_result = extract_text_from_image(contents, filename=file.filename or "")
    extracted_fields = extract_trip_fields(ocr_result["text"], fallback_confidence=ocr_result["confidence"])
    
    trip = normalize_trip_dict(extracted_fields)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO trips (
        trip_id, occurred_at, zone, city, vendor, vehicle_type, trip_type,
        distance_km, claimed_fare_inr, ocr_confidence, ocr_text, raw_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trip["trip_id"], trip["occurred_at"], trip["zone"], trip["city"],
        trip["vendor"], trip["vehicle_type"], trip["trip_type"],
        trip["distance_km"], trip["claimed_fare_inr"], trip["ocr_confidence"],
        trip["ocr_text"], json.dumps(trip)
    ))
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "trip": trip,
        "ocr_confidence": ocr_result["confidence"],
        "is_acceptable": ocr_result["is_acceptable"]
    }


@router.post("/policy")
def ingest_policy(text: str = Form(...), vendor: str = Form("Swiggy"), zone: str = Form("METRO")) -> Dict[str, Any]:
    """Store raw policy text, parse into clauses, and save to database."""
    clauses = parse_raw_policy_text(text, vendor, zone)
    conn = get_connection()
    cursor = conn.cursor()
    for c in clauses:
        cursor.execute("""
        INSERT OR REPLACE INTO clauses (
            clause_id, text, platform_vendor, zone, effective_from, effective_to, source_reference, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["clause_id"], c["text"], c["platform_vendor"], c["zone"],
            c["effective_from"], c["effective_to"], c["source_reference"],
            json.dumps(c.get("tags", []))
        ))
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "clauses_created": len(clauses),
        "clause_ids": [c["clause_id"] for c in clauses]
    }
