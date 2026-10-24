"""Unit tests for Decimal math engine and INR 1.00 tolerance boundary."""

import pytest
from decimal import Decimal
from backend.app.calc.engine import compute_fare, round_inr
from backend.app.calc.compare import compare_amounts


@pytest.fixture
def swiggy_rule_card():
    return {
        "rule_id": "RULE-SWIGGY-MAA-2026-V1",
        "version": 1,
        "status": "reviewed",
        "clause_id": "CLAUSE-SWIGGY-MAA-2026",
        "formula": {
            "base_fare_inr": "25.00",
            "per_km_inr": "8.00",
            "night_multiplier": "1.25",
            "airport_surcharge_inr": "0.00",
            "wait_per_min_inr": "1.50",
            "max_toll_inr": "100.00",
            "max_parking_inr": "50.00",
            "vehicle_multipliers": {
                "hatchback": "1.00",
                "sedan": "1.20",
                "suv": "1.50"
            }
        }
    }


def test_standard_synthetic_formula(swiggy_rule_card):
    # Trip: 6.2 km, hatchback, day -> Base 25.00 + (6.2 * 8.00 = 49.60) = 74.60
    trip = {"distance_km": "6.2", "vehicle_type": "hatchback", "is_night": False}
    total, breakdown = compute_fare(trip, swiggy_rule_card)
    assert total == Decimal("74.60")
    assert breakdown["computed_total_inr"] == "74.60"


def test_exact_one_rupee_boundary():
    # Difference of exactly ₹1.00 is MATCH (noise filtered)
    claimed = Decimal("73.60")
    computed = Decimal("74.60")
    paise = 7460
    verdict, diff, _ = compare_amounts(claimed, computed, paise)
    assert verdict == "MATCH"
    assert diff == Decimal("1.00")


def test_just_over_one_rupee_boundary():
    # Difference of ₹1.01 is DISCREPANCY
    claimed = Decimal("73.59")
    computed = Decimal("74.60")
    paise = 7460
    verdict, diff, _ = compare_amounts(claimed, computed, paise)
    assert verdict == "DISCREPANCY"
    assert diff == Decimal("1.01")


def test_night_multiplier(swiggy_rule_card):
    # Night trip: Core 74.60 * 1.25 = 93.25
    trip = {"distance_km": "6.2", "vehicle_type": "hatchback", "is_night": True}
    total, breakdown = compute_fare(trip, swiggy_rule_card)
    assert total == Decimal("93.25")
    assert breakdown["is_night"] is True


def test_vehicle_multiplier(swiggy_rule_card):
    # Sedan multiplier 1.20: Base 25.00 + (5.0 * 8.00 * 1.20 = 48.00) = 73.00
    trip = {"distance_km": "5.0", "vehicle_type": "sedan", "is_night": False}
    total, breakdown = compute_fare(trip, swiggy_rule_card)
    assert total == Decimal("73.00")


def test_toll_cap(swiggy_rule_card):
    # Claimed toll 150.00, cap is 100.00
    trip = {"distance_km": "0.0", "claimed_toll_inr": "150.00"}
    total, breakdown = compute_fare(trip, swiggy_rule_card)
    assert breakdown["allowed_toll_inr"] == "100.00"
    assert total == Decimal("125.00")  # 25 base + 100 toll
