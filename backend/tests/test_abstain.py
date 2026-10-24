"""Abstention and quarantine tests."""

from backend.app.language.abstain import should_abstain_from_trip
from backend.app.pipeline import run_audit


def test_low_ocr_confidence_abstain():
    trip = {
        "trip_id": "T-LOW-OCR",
        "distance_km": "6.2",
        "claimed_fare_inr": "50.00",
        "ocr_confidence": 0.65
    }
    abstain, reason = should_abstain_from_trip(trip)
    assert abstain is True
    assert "below required" in reason

    finding = run_audit("T-LOW-OCR", trip_data=trip)
    assert finding.verdict == "CANNOT_DETERMINE"
    assert "QUARANTINED" in finding.reason


def test_missing_distance_abstain():
    trip = {
        "trip_id": "T-NO-DIST",
        "distance_km": "",
        "claimed_fare_inr": "50.00",
        "ocr_confidence": 0.95
    }
    abstain, reason = should_abstain_from_trip(trip)
    assert abstain is True
    assert "distance_km" in reason


def test_missing_claimed_fare_abstain():
    trip = {
        "trip_id": "T-NO-FARE",
        "distance_km": "5.0",
        "claimed_fare_inr": "",
        "ocr_confidence": 0.95
    }
    abstain, reason = should_abstain_from_trip(trip)
    assert abstain is True
    assert "claimed_fare_inr" in reason


def test_unknown_platform_pipeline_abstain():
    trip = {
        "trip_id": "T-UNKNOWN-PLATFORM",
        "vendor": "FakeCourierXYZ",
        "zone": "NOWHERE",
        "distance_km": "5.0",
        "claimed_fare_inr": "50.00",
        "ocr_confidence": 0.95
    }
    finding = run_audit("T-UNKNOWN-PLATFORM", trip_data=trip)
    assert finding.verdict == "CANNOT_DETERMINE"
