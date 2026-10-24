"""Seeded dataset generator for synthetic_40.csv and ground_truth.csv."""

import csv
from pathlib import Path


def generate_datasets(output_dir: str = "data/trips") -> None:
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)

    trips = []
    ground_truth = []

    # 40 Trips: 38 Planted Discrepancies, 2 Decoys (within ₹1.00)
    for i in range(1, 41):
        trip_id = f"TRIP-{1000 + i}"
        dist = 3.0 + (i * 0.5)  # e.g., 3.5 km, 4.0 km, etc.
        # Rule: Base 25.00 + (dist * 8.00)
        expected = 25.00 + (dist * 8.00)

        if i == 5:
            # Decoy 1: Paid differs by ₹0.50 -> MATCH
            paid = expected - 0.50
            verdict = "MATCH"
            planted = "none_decoy_rounding_50paise"
        elif i == 20:
            # Decoy 2: Paid exact match -> MATCH
            paid = expected
            verdict = "MATCH"
            planted = "none_decoy_exact_match"
        else:
            # Planted discrepancy: underpaid by between ₹12.00 and ₹45.00
            underpay = 10.00 + (i * 1.00)
            paid = max(15.00, round(expected - underpay, 2))
            verdict = "DISCREPANCY"
            planted = f"planted_underpayment_inr_{underpay:.2f}"

        trips.append({
            "trip_id": trip_id,
            "employee_id": f"EMP-{(i % 8) + 1:03d}",
            "occurred_at": f"2026-05-10T{(10 + (i % 12)):02d}:30:00Z",
            "zone": "METRO",
            "city": "Chennai",
            "vendor": "Swiggy",
            "vehicle_type": "hatchback",
            "trip_type": "local",
            "distance_km": f"{dist:.1f}",
            "claimed_fare_inr": f"{paid:.2f}",
            "claimed_toll_inr": "0.00",
            "claimed_parking_inr": "0.00",
            "claimed_wait_inr": "0.00",
            "wait_minutes": "0",
            "is_night": "False",
            "ocr_confidence": "0.98",
            "ocr_text": f"Trip {trip_id} receipt distance {dist:.1f}km paid INR {paid:.2f}",
            "notes": "Regular shift trip",
            "planted_error": planted
        })

        ground_truth.append({
            "trip_id": trip_id,
            "expected_verdict": verdict,
            "expected_computed_inr": f"{expected:.2f}",
            "paid_fare_inr": f"{paid:.2f}",
            "planted_error": planted
        })

    # Write synthetic_40.csv
    synth_path = p / "synthetic_40.csv"
    with open(synth_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(trips[0].keys()))
        writer.writeheader()
        writer.writerows(trips)

    # Write ground_truth.csv
    gt_path = p / "ground_truth.csv"
    with open(gt_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(ground_truth[0].keys()))
        writer.writeheader()
        writer.writerows(ground_truth)

    # Write extras_edge_cases.csv
    # Edge cases:
    # 1. Exact ₹1.00 boundary (MATCH)
    # 2. Just over ₹1.00 boundary (₹1.01 difference -> DISCREPANCY)
    # 3. Degraded unreadable receipt (confidence 0.60 -> CANNOT_DETERMINE)
    # 4. Unknown platform (CANNOT_DETERMINE)
    # 5. Missing distance (CANNOT_DETERMINE)
    extras = [
        {
            "trip_id": "TRIP-EDGE-01",
            "employee_id": "EMP-999",
            "occurred_at": "2026-05-10T12:00:00Z",
            "zone": "METRO",
            "city": "Chennai",
            "vendor": "Swiggy",
            "vehicle_type": "hatchback",
            "trip_type": "local",
            "distance_km": "5.0",
            "claimed_fare_inr": "64.00",  # Expected: 25 + 40 = 65.00 -> Diff: 1.00 (MATCH)
            "claimed_toll_inr": "0.00",
            "claimed_parking_inr": "0.00",
            "claimed_wait_inr": "0.00",
            "wait_minutes": "0",
            "is_night": "False",
            "ocr_confidence": "0.95",
            "ocr_text": "Exact 1.00 boundary",
            "notes": "Boundary test exact ₹1.00",
            "planted_error": "exact_1_inr_boundary"
        },
        {
            "trip_id": "TRIP-EDGE-02",
            "employee_id": "EMP-999",
            "occurred_at": "2026-05-10T12:00:00Z",
            "zone": "METRO",
            "city": "Chennai",
            "vendor": "Swiggy",
            "vehicle_type": "hatchback",
            "trip_type": "local",
            "distance_km": "5.0",
            "claimed_fare_inr": "63.99",  # Expected: 65.00 -> Diff: 1.01 (DISCREPANCY)
            "claimed_toll_inr": "0.00",
            "claimed_parking_inr": "0.00",
            "claimed_wait_inr": "0.00",
            "wait_minutes": "0",
            "is_night": "False",
            "ocr_confidence": "0.95",
            "ocr_text": "Just over 1.00 boundary",
            "notes": "Boundary test ₹1.01",
            "planted_error": "just_over_1_inr_boundary"
        },
        {
            "trip_id": "TRIP-EDGE-03-DEGRADED",
            "employee_id": "EMP-999",
            "occurred_at": "2026-05-10T12:00:00Z",
            "zone": "METRO",
            "city": "Chennai",
            "vendor": "Swiggy",
            "vehicle_type": "hatchback",
            "trip_type": "local",
            "distance_km": "5.0",
            "claimed_fare_inr": "50.00",
            "claimed_toll_inr": "0.00",
            "claimed_parking_inr": "0.00",
            "claimed_wait_inr": "0.00",
            "wait_minutes": "0",
            "is_night": "False",
            "ocr_confidence": "0.55",  # Below 0.80 -> CANNOT_DETERMINE
            "ocr_text": "BLURRY UNREADABLE RECEIPT",
            "notes": "Degraded OCR case",
            "planted_error": "low_ocr_confidence_quarantine"
        },
        {
            "trip_id": "TRIP-EDGE-04-UNKNOWN-PLATFORM",
            "employee_id": "EMP-999",
            "occurred_at": "2026-05-10T12:00:00Z",
            "zone": "METRO",
            "city": "Chennai",
            "vendor": "NonExistentVendor",
            "vehicle_type": "hatchback",
            "trip_type": "local",
            "distance_km": "5.0",
            "claimed_fare_inr": "50.00",
            "claimed_toll_inr": "0.00",
            "claimed_parking_inr": "0.00",
            "claimed_wait_inr": "0.00",
            "wait_minutes": "0",
            "is_night": "False",
            "ocr_confidence": "0.95",
            "ocr_text": "Unknown vendor test",
            "notes": "No policy fixture available",
            "planted_error": "missing_policy_fixture"
        }
    ]

    extras_path = p / "extras_edge_cases.csv"
    with open(extras_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(extras[0].keys()))
        writer.writeheader()
        writer.writerows(extras)


if __name__ == "__main__":
    generate_datasets()
    print("Seeded datasets generated in data/trips/")
