"""Pydantic models strictly matching contracts/ JSON Schema."""

from typing import Literal, Optional, Any, Dict, List
from pydantic import BaseModel, Field

Verdict = Literal["MATCH", "DISCREPANCY", "CANNOT_DETERMINE"]
ReviewStatus = Literal["pending", "approved", "rejected"]
Zone = Literal["METRO", "TIER2"]
VehicleType = Literal["hatchback", "sedan", "suv"]
TripType = Literal["local", "airport", "outstation"]


class Trip(BaseModel):
    trip_id: str
    employee_id: Optional[str] = None
    occurred_at: Optional[str] = None
    zone: Optional[str] = "METRO"
    city: Optional[str] = None
    vendor: Optional[str] = "Swiggy"
    vehicle_type: Optional[str] = "hatchback"
    trip_type: Optional[str] = "local"
    distance_km: Optional[str] = "0.00"
    claimed_fare_inr: Optional[str] = "0.00"
    claimed_toll_inr: Optional[str] = "0.00"
    claimed_parking_inr: Optional[str] = "0.00"
    claimed_wait_inr: Optional[str] = "0.00"
    wait_minutes: Optional[str] = "0"
    is_night: Optional[bool] = False
    ocr_confidence: Optional[float] = 1.0
    ocr_text: Optional[str] = None
    notes: Optional[str] = None
    planted_error: Optional[str] = None


class RuleCardFormula(BaseModel):
    base_fare_inr: str = "25.00"
    per_km_inr: str = "8.00"
    night_multiplier: str = "1.00"
    airport_surcharge_inr: str = "0.00"
    wait_per_min_inr: str = "0.00"
    max_toll_inr: str = "100.00"
    max_parking_inr: str = "50.00"
    vehicle_multipliers: Dict[str, str] = Field(
        default_factory=lambda: {"hatchback": "1.00", "sedan": "1.20", "suv": "1.50"}
    )


class RuleCard(BaseModel):
    rule_id: str
    version: int = 1
    status: Literal["reviewed"] = "reviewed"
    clause_id: str
    zone: Optional[str] = "METRO"
    trip_type: Optional[str] = "local"
    effective_from: str = "2026-01-01T00:00:00Z"
    effective_to: Optional[str] = None
    formula: RuleCardFormula = Field(default_factory=RuleCardFormula)


class Finding(BaseModel):
    finding_id: str
    trip_id: str
    verdict: Verdict
    claimed_fare_inr: Optional[str] = None
    computed_fare_inr: Optional[str] = None
    verified_fare_inr: Optional[str] = None
    engine_delta_inr: Optional[str] = None
    tolerance_inr: str = "1.00"
    rule_id: Optional[str] = None
    clause_id: Optional[str] = None
    evidence_packet_id: Optional[str] = None
    review_status: ReviewStatus = "pending"
    reason: Optional[str] = None
    breakdown: Optional[Dict[str, Any]] = None
    execution_log: Optional[List[str]] = None


class LedgerEvent(BaseModel):
    event_id: str
    finding_id: Optional[str] = None
    payload: Dict[str, Any]
    prev_hash: str
    event_hash: str
    timestamp: Optional[str] = None


class QuarantineItem(BaseModel):
    id: Optional[int] = None
    trip_id: str
    reason: str
    ocr_confidence: Optional[float] = None
    payload: Dict[str, Any]
    quarantined_at: Optional[str] = None
