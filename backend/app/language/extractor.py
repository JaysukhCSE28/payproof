"""Fields and evidence span extractor with confidence."""

import re
from typing import Dict, Any
from backend.app.language.gemini_client import extract_with_gemini
from backend.app.evidence.normalizer import clean_currency_str, clean_number_str


def extract_trip_fields(raw_text: str, fallback_confidence: float = 0.95) -> Dict[str, Any]:
    """
    Extract structured fields from unformatted text using regex or optional Gemini.
    Returns normalized trip dictionary with confidence.
    """
    gemini_result = extract_with_gemini(raw_text)
    if gemini_result:
        gemini_result["provenance"] = "GEMINI_EXTRACTION"
        gemini_result["ocr_confidence"] = fallback_confidence
        return gemini_result

    # Deterministic regex extraction
    trip_id_match = re.search(r"TRIP[-_]?\w+", raw_text, re.IGNORECASE)
    dist_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kms)", raw_text, re.IGNORECASE)
    fare_match = re.search(r"(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d+)?)", raw_text, re.IGNORECASE)

    trip_id = trip_id_match.group(0).upper() if trip_id_match else "TRIP-MANUAL"
    distance = dist_match.group(1) if dist_match else "0.00"
    fare = fare_match.group(1) if fare_match else "0.00"

    return {
        "trip_id": trip_id,
        "distance_km": clean_number_str(distance),
        "claimed_fare_inr": clean_currency_str(fare),
        "ocr_confidence": fallback_confidence,
        "ocr_text": raw_text,
        "provenance": "REGEX_EXTRACTION"
    }
