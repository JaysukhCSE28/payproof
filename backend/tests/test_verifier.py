"""Dual-engine agreement tests between Decimal and integer-paise paths."""

import pytest
from backend.app.calc.engine import compute_fare
from backend.app.calc.verifier import compute_fare_paise


@pytest.fixture
def test_rule():
    return {
        "rule_id": "RULE-TEST",
        "formula": {
            "base_fare_inr": "25.00",
            "per_km_inr": "8.00",
            "night_multiplier": "1.25",
            "airport_surcharge_inr": "50.00",
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


@pytest.mark.parametrize("dist,veh,is_night,ttype,wait,toll,parking", [
    ("6.2", "hatchback", False, "local", "0", "0.00", "0.00"),
    ("10.0", "sedan", True, "airport", "15", "80.00", "30.00"),
    ("3.5", "suv", False, "local", "5", "150.00", "100.00"),
    ("0.0", "hatchback", True, "local", "0", "0.00", "0.00"),
    ("12.7", "sedan", False, "airport", "20", "20.00", "10.00")
])
def test_decimal_and_paise_agreement(test_rule, dist, veh, is_night, ttype, wait, toll, parking):
    trip = {
        "distance_km": dist,
        "vehicle_type": veh,
        "is_night": is_night,
        "trip_type": ttype,
        "wait_minutes": wait,
        "claimed_toll_inr": toll,
        "claimed_parking_inr": parking
    }

    decimal_total, _ = compute_fare(trip, test_rule)
    paise_total = compute_fare_paise(trip, test_rule)

    computed_paise = int(round(decimal_total * 100))
    # Must agree within 1 paisa (rounding boundary)
    assert abs(computed_paise - paise_total) <= 1
