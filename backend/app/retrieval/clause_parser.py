"""Policy text -> clauses parser and loader."""

import json
from pathlib import Path
from typing import List, Dict, Any


def load_clauses(path: str = "data/policy/clauses.json") -> List[Dict[str, Any]]:
    """Load policy clauses from JSON file."""
    p = Path(path)
    if not p.exists():
        return []
    try:
        content = p.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception:
        return []


def parse_raw_policy_text(text: str, vendor: str, zone: str) -> List[Dict[str, Any]]:
    """Parse unformatted raw policy document into clause objects."""
    clauses = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    for i, para in enumerate(paragraphs, 1):
        clause_id = f"CLAUSE-{vendor.upper()}-{zone.upper()}-{i}"
        clauses.append({
            "clause_id": clause_id,
            "text": para,
            "platform_vendor": vendor,
            "zone": zone,
            "effective_from": "2026-01-01T00:00:00Z",
            "effective_to": "2026-12-31T23:59:59Z",
            "source_reference": f"Scraped/Raw Policy: {vendor} {zone}",
            "tags": [vendor.lower(), zone.lower()]
        })
    return clauses
