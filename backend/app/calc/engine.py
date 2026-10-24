"""Primary Decimal-based calculation engine."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, Tuple


def round_inr(val: Decimal) -> Decimal:
    """Explicit half-up rounding to two decimal places."""
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def compute_fare(trip: Dict[str, Any], rule_card: Dict[str, Any]) -> Tuple[Decimal, Dict[str, Any]]:
    """
    Apply reviewed rule-card formula using Decimal only.
    Formula:
      1. Base Fare
      2. Distance Fare = Distance * Per_KM * Vehicle_Multiplier
      3. Subtotal_Pre_Night = Base + Distance Fare
      4. Subtotal_Night = Subtotal_Pre_Night * Night_Multiplier (if is_night) else Subtotal_Pre_Night
      5. Airport Surcharge (if trip_type == 'airport')
      6. Wait Fare = Wait_Minutes * Wait_Per_Min
      7. Toll = min(Claimed_Toll, Max_Toll)
      8. Parking = min(Claimed_Parking, Max_Parking)
      Total = Subtotal_Night + Airport Surcharge + Wait Fare + Toll + Parking
    """
    formula = rule_card.get("formula", {})
    if hasattr(formula, "model_dump"):
        formula = formula.model_dump()

    base_fare = Decimal(str(formula.get("base_fare_inr", "25.00")))
    per_km = Decimal(str(formula.get("per_km_inr", "8.00")))
    
    distance_km = Decimal(str(trip.get("distance_km", "0.00") or "0.00"))
    vehicle_type = str(trip.get("vehicle_type", "hatchback") or "hatchback").lower()
    
    veh_mults = formula.get("vehicle_multipliers", {}) or {}
    veh_mult = Decimal(str(veh_mults.get(vehicle_type, "1.00")))
    
    distance_fare = round_inr(distance_km * per_km * veh_mult)
    subtotal_core = base_fare + distance_fare
    
    # Night multiplier
    is_night_raw = trip.get("is_night", False)
    is_night = is_night_raw in (True, 1, "1", "true", "True")
    if is_night:
        night_mult = Decimal(str(formula.get("night_multiplier", "1.00")))
        subtotal_night = round_inr(subtotal_core * night_mult)
        night_extra = subtotal_night - subtotal_core
    else:
        subtotal_night = subtotal_core
        night_extra = Decimal("0.00")
        
    # Airport surcharge
    trip_type = str(trip.get("trip_type", "local") or "local").lower()
    if trip_type == "airport":
        airport_surcharge = Decimal(str(formula.get("airport_surcharge_inr", "0.00")))
    else:
        airport_surcharge = Decimal("0.00")
        
    # Waiting fare
    wait_min = Decimal(str(trip.get("wait_minutes", "0") or "0"))
    wait_per_min = Decimal(str(formula.get("wait_per_min_inr", "0.00")))
    wait_fare = round_inr(wait_min * wait_per_min)
    
    # Toll with cap
    claimed_toll = Decimal(str(trip.get("claimed_toll_inr", "0.00") or "0.00"))
    max_toll = Decimal(str(formula.get("max_toll_inr", "100.00")))
    allowed_toll = min(claimed_toll, max_toll)
    
    # Parking with cap
    claimed_parking = Decimal(str(trip.get("claimed_parking_inr", "0.00") or "0.00"))
    max_parking = Decimal(str(formula.get("max_parking_inr", "50.00")))
    allowed_parking = min(claimed_parking, max_parking)
    
    total = round_inr(subtotal_night + airport_surcharge + wait_fare + allowed_toll + allowed_parking)
    
    breakdown = {
        "base_fare_inr": str(base_fare),
        "distance_km": str(distance_km),
        "per_km_inr": str(per_km),
        "vehicle_type": vehicle_type,
        "vehicle_multiplier": str(veh_mult),
        "distance_fare_inr": str(distance_fare),
        "is_night": is_night,
        "night_extra_inr": str(night_extra),
        "airport_surcharge_inr": str(airport_surcharge),
        "wait_minutes": str(wait_min),
        "wait_fare_inr": str(wait_fare),
        "allowed_toll_inr": str(allowed_toll),
        "allowed_parking_inr": str(allowed_parking),
        "computed_total_inr": str(total)
    }
    
    return total, breakdown
