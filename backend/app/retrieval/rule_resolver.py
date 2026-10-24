"""Resolve matched clause or metadata to a reviewed, versioned RuleCard."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


def load_rule_cards(path: str = "data/policy/rule_cards.json") -> List[Dict[str, Any]]:
    """Load reviewed rule cards from JSON disk."""
    p = Path(path)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def resolve_rule_card(
    clause_id: Optional[str] = None,
    zone: Optional[str] = None,
    trip_type: Optional[str] = None,
    timestamp: Optional[str] = None,
    path: str = "data/policy/rule_cards.json"
) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Resolve to a single, reviewed, unambiguous rule card.
    If no rule card matches -> return None, reason.
    If ambiguous overlapping rule cards match -> return None, reason (triggers CANNOT_DETERMINE).
    """
    all_rules = load_rule_cards(path)
    reviewed_rules = [r for r in all_rules if r.get("status") == "reviewed"]

    if not reviewed_rules:
        return None, "No reviewed rule cards available."

    # Priority 1: match by clause_id
    if clause_id:
        matches = [r for r in reviewed_rules if r.get("clause_id") == clause_id]
        if len(matches) == 1:
            return matches[0], "Exact clause-to-rule mapping resolved."
        elif len(matches) > 1:
            # Sort by version descending
            sorted_m = sorted(matches, key=lambda x: x.get("version", 1), reverse=True)
            return sorted_m[0], f"Resolved latest version (v{sorted_m[0].get('version')}) for clause {clause_id}."

    # Priority 2: match by zone and trip_type
    candidates = []
    for r in reviewed_rules:
        if zone and r.get("zone", "").upper() != zone.upper():
            continue
        if trip_type and r.get("trip_type", "").lower() != trip_type.lower():
            continue
        # Check temporal window if timestamp provided
        if timestamp:
            eff_from = r.get("effective_from")
            eff_to = r.get("effective_to")
            if eff_from and timestamp < eff_from:
                continue
            if eff_to and timestamp > eff_to:
                continue
        candidates.append(r)

    if len(candidates) == 1:
        return candidates[0], "Unambiguous metadata match resolved."
    elif len(candidates) == 0:
        return None, f"No reviewed rule card matches zone='{zone}', trip_type='{trip_type}'."
    else:
        # Check if they have the same rule_id with different versions
        rule_ids = set(r.get("rule_id") for r in candidates)
        if len(rule_ids) == 1:
            sorted_candidates = sorted(candidates, key=lambda x: x.get("version", 1), reverse=True)
            return sorted_candidates[0], f"Resolved latest version (v{sorted_candidates[0].get('version')})."
        return None, f"Ambiguous policy conflict: {len(candidates)} distinct rule cards match query."
