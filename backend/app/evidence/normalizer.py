"""Currency, unit cleanup, and Decimal string coercion."""

import re
from typing import Dict, Any


def clean_currency_str(val: Any) -> str:
    """Strip currency symbols (₹, Rs, INR, commas) and return clean Decimal string."""
    if val is None:
        return "0.00"
    s = str(val).strip()
    s = re.sub(r"[₹RsINR,\s]", "", s, flags=re.IGNORECASE)
    if not s:
        return "0.00"
    try:
        float(s)
        if "." in s:
            p = s.split(".")
            return f"{p[0]}.{p[1][:2].ljust(2, '0')}"
        return f"{s}.00"
    except ValueError:
        return "0.00"


def clean_number_str(val: Any) -> str:
    """Strip units (km, min) and return valid numeric string."""
    if val is None:
        return "0"
    s = str(val).strip()
    s = re.sub(r"[a-zA-Z,\s]", "", s)
    return s if s else "0"


def normalize_trip_dict(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw dictionary into trip schema compliant format."""
    trip_id = str(raw.get("trip_id", "")).strip()
    zone = str(raw.get("zone", "METRO") or "METRO").upper().strip()
    if zone not in ("METRO", "TIER2"):
        zone = "METRO"

    vehicle_type = str(raw.get("vehicle_type", "hatchback") or "hatchback").lower().strip()
    if vehicle_type not in ("hatchback", "sedan", "suv"):
        vehicle_type = "hatchback"

    trip_type = str(raw.get("trip_type", "local") or "local").lower().strip()
    if trip_type not in ("local", "airport", "outstation"):
        trip_type = "local"

    is_night_raw = raw.get("is_night", False)
    is_night = is_night_raw in (True, 1, "1", "true", "True", "yes", "YES")

    ocr_conf_raw = raw.get("ocr_confidence", 1.0)
    try:
        ocr_confidence = float(ocr_conf_raw) if ocr_conf_raw is not None else 1.0
    except (ValueError, TypeError):
        ocr_confidence = 1.0

    return {
        "trip_id": trip_id,
        "employee_id": str(raw.get("employee_id", "") or "").strip(),
        "occurred_at": str(raw.get("occurred_at", "2026-05-10T12:00:00Z") or "2026-05-10T12:00:00Z").strip(),
        "zone": zone,
        "city": str(raw.get("city", "Chennai") or "Chennai").strip(),
        "vendor": str(raw.get("vendor", "Swiggy") or "Swiggy").strip(),
        "vehicle_type": vehicle_type,
        "trip_type": trip_type,
        "distance_km": clean_number_str(raw.get("distance_km", "0.00")),
        "claimed_fare_inr": clean_currency_str(raw.get("claimed_fare_inr", "0.00")),
        "claimed_toll_inr": clean_currency_str(raw.get("claimed_toll_inr", "0.00")),
        "claimed_parking_inr": clean_currency_str(raw.get("claimed_parking_inr", "0.00")),
        "claimed_wait_inr": clean_currency_str(raw.get("claimed_wait_inr", "0.00")),
        "wait_minutes": clean_number_str(raw.get("wait_minutes", "0")),
        "is_night": is_night,
        "ocr_confidence": ocr_confidence,
        "ocr_text": str(raw.get("ocr_text", "") or ""),
        "notes": str(raw.get("notes", "") or ""),
        "planted_error": str(raw.get("planted_error", "") or "")
    }
