"""Policy clause retrieval and provenance tests."""

from backend.app.retrieval.retriever import PolicyRetriever


def test_metadata_clause_retrieval():
    retriever = PolicyRetriever()
    trip = {
        "vendor": "Swiggy",
        "zone": "METRO",
        "trip_type": "local",
        "occurred_at": "2026-05-10T12:00:00Z"
    }
    clause, rule_card, msg = retriever.retrieve(trip)
    assert clause is not None
    assert clause["clause_id"] == "CLAUSE-SWIGGY-MAA-2026"
    assert rule_card is not None
    assert rule_card["rule_id"] == "RULE-SWIGGY-MAA-2026-V1"
    assert "Swiggy" in clause["source_reference"]


def test_temporal_out_of_bounds_retrieval():
    retriever = PolicyRetriever()
    # Trip in 2028 when 2026 policy is expired
    trip = {
        "vendor": "Swiggy",
        "zone": "METRO",
        "trip_type": "local",
        "occurred_at": "2028-05-10T12:00:00Z"
    }
    clause, rule_card, msg = retriever.retrieve(trip)
    # Temporal filtering should prevent exact match, or rule resolution should note expiry
    assert rule_card is None or "BM25" in msg or "No" in msg


def test_unknown_vendor_retrieval():
    retriever = PolicyRetriever()
    trip = {
        "vendor": "AlienLogistics",
        "zone": "MARS",
        "trip_type": "space",
        "occurred_at": "2026-05-10T12:00:00Z"
    }
    clause, rule_card, msg = retriever.retrieve(trip)
    # Cannot resolve a reviewed rule card
    assert rule_card is None
