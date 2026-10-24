"""Hybrid policy search combining metadata filtering and BM25 index."""

from typing import Dict, Any, Optional, Tuple
from backend.app.retrieval.clause_parser import load_clauses
from backend.app.retrieval.index import ClauseIndex
from backend.app.retrieval.rule_resolver import resolve_rule_card


class PolicyRetriever:
    def __init__(self, clauses_path: str = "data/policy/clauses.json", rules_path: str = "data/policy/rule_cards.json"):
        self.clauses_path = clauses_path
        self.rules_path = rules_path
        self.reload()

    def reload(self) -> None:
        self.clauses = load_clauses(self.clauses_path)
        self.index = ClauseIndex(self.clauses)

    def retrieve(self, trip: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], str]:
        """
        1. Filter clauses by platform_vendor and zone.
        2. Filter by temporal validity.
        3. If multiple remain, rank using BM25 query over trip metadata.
        4. Resolve matching rule card.
        Returns: (matched_clause, matched_rule_card, explanation)
        """
        vendor = str(trip.get("vendor", "")).strip().lower()
        zone = str(trip.get("zone", "")).strip().upper()
        trip_type = str(trip.get("trip_type", "local")).strip().lower()
        timestamp = str(trip.get("occurred_at", "")).strip()

        # Guard: if trip vendor is specified but matches NO clause vendor → CANNOT_DETERMINE
        if vendor:
            known_vendors = {str(c.get("platform_vendor", "")).lower() for c in self.clauses if c.get("platform_vendor")}
            if vendor not in known_vendors:
                return None, None, f"Vendor '{vendor}' is not covered by any reviewed policy clause."

        # Step 1: Metadata candidates
        candidates = []
        for c in self.clauses:
            c_vendor = str(c.get("platform_vendor", "")).lower()
            c_zone = str(c.get("zone", "")).upper()
            if vendor and c_vendor and vendor != c_vendor:
                continue
            if zone and c_zone and zone != c_zone:
                continue
            # Temporal check
            eff_from = c.get("effective_from")
            eff_to = c.get("effective_to")
            if timestamp and eff_from and timestamp < eff_from:
                continue
            if timestamp and eff_to and timestamp > eff_to:
                continue
            candidates.append(c)

        if not candidates:
            # Fallback to BM25 query — only accept if at least one query token matches corpus
            query = f"{vendor} {zone} {trip_type}"
            query_tokens = set(query.lower().split())
            bm25_matches = self.index.search(query, top_k=1)

            # Reject fallback match if no query token overlaps with matched clause text/tags
            if bm25_matches:
                clause_text = (bm25_matches[0].get("text", "") + " " + " ".join(bm25_matches[0].get("tags", []))).lower()
                clause_tokens = set(clause_text.split())
                if not query_tokens.intersection(clause_tokens):
                    bm25_matches = []  # No meaningful overlap → treat as no match

            if not bm25_matches:
                return None, None, f"No policy clause matched vendor='{vendor}', zone='{zone}', timestamp='{timestamp}'."
            matched_clause = bm25_matches[0]
            expl = f"BM25 match (Score-ranked) for '{query}'."
        elif len(candidates) == 1:
            matched_clause = candidates[0]
            expl = f"Exact metadata match: {matched_clause.get('clause_id')}."
        else:
            # Rank candidates by trip_type tag or BM25
            sub_index = ClauseIndex(candidates)
            query = f"{vendor} {zone} {trip_type}"
            ranked = sub_index.search(query, top_k=1)
            matched_clause = ranked[0] if ranked else candidates[0]
            expl = f"Filtered {len(candidates)} candidates -> selected {matched_clause.get('clause_id')}."

        # Step 2: Resolve to reviewed rule card
        rule_card, rule_msg = resolve_rule_card(
            clause_id=matched_clause.get("clause_id"),
            zone=zone,
            trip_type=trip_type,
            timestamp=timestamp,
            path=self.rules_path
        )

        if not rule_card:
            return matched_clause, None, f"Clause {matched_clause.get('clause_id')} found, but: {rule_msg}"

        return matched_clause, rule_card, f"{expl} Resolved Rule Card: {rule_card.get('rule_id')} (v{rule_card.get('version')})."
