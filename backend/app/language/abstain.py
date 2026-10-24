"""Abstention rules forcing CANNOT_DETERMINE."""

from typing import Dict, Any, Tuple
from backend.app.config import settings


def should_abstain_from_trip(trip: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Evaluate whether audit must immediately abstain with CANNOT_DETERMINE:
    1. OCR confidence below minimum threshold (0.80)
    2. Missing trip_id
    3. Missing or invalid distance
    4. Missing or invalid claimed fare
    """
    ocr_conf = trip.get("ocr_confidence")
    if ocr_conf is not None:
        try:
            if float(ocr_conf) < settings.ocr_min_confidence:
                return True, f"OCR confidence ({float(ocr_conf)*100:.1f}%) is below required {settings.ocr_min_confidence*100:.1f}% threshold."
        except (ValueError, TypeError):
            return True, "Invalid OCR confidence value."

    trip_id = trip.get("trip_id")
    if not trip_id or str(trip_id).strip() == "":
        return True, "Missing required field: trip_id."

    dist_str = str(trip.get("distance_km", "")).strip()
    if not dist_str:
        return True, "Missing required field: distance_km."
    try:
        dist = float(dist_str)
        if dist < 0:
            return True, "Invalid negative distance."
    except ValueError:
        return True, f"Unparseable distance value: {dist_str}"

    fare_str = str(trip.get("claimed_fare_inr", "")).strip()
    if not fare_str:
        return True, "Missing required field: claimed_fare_inr."
    try:
        fare = float(fare_str)
        if fare < 0:
            return True, "Invalid negative claimed fare."
    except ValueError:
        return True, f"Unparseable claimed fare value: {fare_str}"

    return False, ""
