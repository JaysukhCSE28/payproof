"""CSV ingestion and validation against trip.schema.json."""

import csv
import io
from pathlib import Path
from typing import List, Dict, Any, Union
from backend.app.evidence.normalizer import normalize_trip_dict


def parse_csv_content(content: str) -> List[Dict[str, Any]]:
    """Parse CSV text content into normalized trip dictionaries."""
    f = io.StringIO(content.strip())
    reader = csv.DictReader(f)
    trips: List[Dict[str, Any]] = []
    for row in reader:
        cleaned = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items() if k}
        if not cleaned.get("trip_id"):
            continue
        trips.append(normalize_trip_dict(cleaned))
    return trips


def load_trips_csv(path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Parse CSV file from disk, coerce decimals as strings, validate required fields."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    text = p.read_text(encoding="utf-8")
    return parse_csv_content(text)
