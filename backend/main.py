import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

# Also import full architecture routers & database
from backend.app.db import get_connection, init_schema
from backend.app.routers import ingest, audit, review, ledger

# Initialize database schema
conn = get_connection()
init_schema(conn)
conn.close()

app = FastAPI(title="PayProof Deterministic Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount full system routers
app.include_router(ingest.router)
app.include_router(audit.router)
app.include_router(review.router)
app.include_router(ledger.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "system": "PayProof Deterministic Engine", "version": "1.0.0"}


# In-memory ledger & cache for rapid prototype testing
AUDIT_CACHE = {}
LEDGER_CHAIN = []

class TripRecord(BaseModel):
    trip_id: str
    distance_km: float
    paid_amount: float
    ocr_confidence: float = 0.95

# Synthetic Rate Card Policy
class PolicyFixture:
    base_pay = Decimal("25.00")
    per_km_rate = Decimal("8.00")
    rain_bonus = Decimal("12.50")

def round_inr(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@app.post("/api/audit")
def audit_trip(trip: TripRecord):
    # 1. Pessimistic Confidence Gate
    if trip.ocr_confidence < 0.80:
        return {"status": "CANNOT_DETERMINE", "reason": f"OCR confidence {trip.ocr_confidence} is too low."}

    # 2. Deterministic Math Sandbox (No LLM Math)
    distance_pay = Decimal(str(trip.distance_km)) * PolicyFixture.per_km_rate
    expected_pay = round_inr(PolicyFixture.base_pay + distance_pay + PolicyFixture.rain_bonus)
    paid = round_inr(Decimal(str(trip.paid_amount)))
    difference = expected_pay - paid

    # 3. Noise Tolerance Filter (ignores differences under ₹1.00)
    status = "MATCH" if abs(difference) <= Decimal("1.00") else "DISCREPANCY"

    result = {
        "trip_id": trip.trip_id,
        "expected_pay": float(expected_pay),
        "paid_amount": float(paid),
        "difference": float(difference),
        "status": status,
        "approved": False
    }
    
    AUDIT_CACHE[trip.trip_id] = result
    return result

@app.post("/api/ledger/approve/{trip_id}")
def approve_to_ledger(trip_id: str):
    if trip_id not in AUDIT_CACHE:
        raise HTTPException(status_code=404, detail="Audit not found")
        
    audit_data = AUDIT_CACHE[trip_id]
    audit_data["approved"] = True
    
    # 4. RFC 8785 SHA-256 Hash Chaining
    prev_hash = LEDGER_CHAIN[-1]["current_hash"] if LEDGER_CHAIN else "0" * 64
    canonical_payload = json.dumps(audit_data, sort_keys=True, separators=(',', ':'))
    timestamp = datetime.now(timezone.utc).isoformat()
    
    raw_str = f"{prev_hash}|{canonical_payload}|{timestamp}".encode('utf-8')
    current_hash = hashlib.sha256(raw_str).hexdigest()
    
    block = {
        "block_index": len(LEDGER_CHAIN) + 1,
        "trip_id": trip_id,
        "previous_hash": prev_hash,
        "current_hash": current_hash,
        "timestamp": timestamp
    }
    
    LEDGER_CHAIN.append(block)
    return block

@app.get("/api/ledger")
def get_ledger():
    return LEDGER_CHAIN