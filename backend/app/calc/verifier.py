"""Independent integer-paise calculation path."""

from typing import Dict, Any


def to_paise(val_str: Any) -> int:
    """Safely convert decimal string representation of INR to integer paise."""
    s = str(val_str or "0.00").strip()
    if "." in s:
        parts = s.split(".")
        rupees = int(parts[0]) if parts[0] else 0
        dec = parts[1][:2].ljust(2, "0")
        cents = int(dec)
        sign = -1 if s.startswith("-") else 1
        return rupees * 100 + (sign * cents)
    return int(s or "0") * 100


def compute_fare_paise(trip: Dict[str, Any], rule_card: Dict[str, Any]) -> int:
    """
    Recompute the same formula in integer paise (no Decimal, no float math).
    Paise: 1 INR = 100 paise.
    """
    formula = rule_card.get("formula", {})
    if hasattr(formula, "model_dump"):
        formula = formula.model_dump()

    base_p = to_paise(formula.get("base_fare_inr", "25.00"))
    per_km_p = to_paise(formula.get("per_km_inr", "8.00"))

    # Distance in hundredths of km (e.g. 6.20 km -> 620)
    dist_str = str(trip.get("distance_km", "0.00") or "0.00").strip()
    if "." in dist_str:
        p = dist_str.split(".")
        dist_units = int(p[0]) * 100 + int(p[1][:2].ljust(2, "0"))
    else:
        dist_units = int(dist_str or "0") * 100

    vehicle_type = str(trip.get("vehicle_type", "hatchback") or "hatchback").lower()
    veh_mults = formula.get("vehicle_multipliers", {}) or {}
    # Multiplier in hundredths (e.g. "1.20" -> 120, "1.00" -> 100)
    veh_mult_str = str(veh_mults.get(vehicle_type, "1.00"))
    veh_mult_factor = int(round(float(veh_mult_str) * 100))

    # dist_fare_paise = (dist_units * per_km_p * veh_mult_factor) // (100 * 100)
    # Using half-up integer rounding: (x + 50) // 100
    num = dist_units * per_km_p * veh_mult_factor
    denom = 10000
    dist_fare_p = (num + (denom // 2)) // denom

    subtotal_core_p = base_p + dist_fare_p

    is_night_raw = trip.get("is_night", False)
    is_night = is_night_raw in (True, 1, "1", "true", "True")
    if is_night:
        night_mult_str = str(formula.get("night_multiplier", "1.00"))
        night_mult_factor = int(round(float(night_mult_str) * 100))
        subtotal_night_p = (subtotal_core_p * night_mult_factor + 50) // 100
    else:
        subtotal_night_p = subtotal_core_p

    trip_type = str(trip.get("trip_type", "local") or "local").lower()
    if trip_type == "airport":
        airport_p = to_paise(formula.get("airport_surcharge_inr", "0.00"))
    else:
        airport_p = 0

    wait_min = int(float(str(trip.get("wait_minutes", "0") or "0")))
    wait_per_min_p = to_paise(formula.get("wait_per_min_inr", "0.00"))
    wait_p = wait_min * wait_per_min_p

    claimed_toll_p = to_paise(trip.get("claimed_toll_inr", "0.00"))
    max_toll_p = to_paise(formula.get("max_toll_inr", "100.00"))
    toll_p = min(claimed_toll_p, max_toll_p)

    claimed_parking_p = to_paise(trip.get("claimed_parking_inr", "0.00"))
    max_parking_p = to_paise(formula.get("max_parking_inr", "50.00"))
    parking_p = min(claimed_parking_p, max_parking_p)

    total_paise = subtotal_night_p + airport_p + wait_p + toll_p + parking_p
    return total_paise
