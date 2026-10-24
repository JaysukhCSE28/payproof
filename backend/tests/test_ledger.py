"""Tamper-evident ledger append and chain verification tests."""

from backend.app.db import get_connection, init_schema
from backend.app.ledger.chain import append_to_ledger, verify_chain, tamper_ledger_entry
from backend.app.ledger.canonical import canonicalize


def test_canonical_json_determinism():
    d1 = {"b": 2, "a": 1, "nested": {"z": 26, "y": 25}}
    d2 = {"nested": {"y": 25, "z": 26}, "a": 1, "b": 2}
    # Enforces sorted keys and compact formatting
    assert canonicalize(d1) == canonicalize(d2)
    assert " " not in canonicalize(d1)


def test_ledger_append_and_tamper_detection():
    conn = get_connection()
    init_schema(conn)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ledger")
    conn.commit()
    conn.close()

    # Step 1: Append two events
    e1 = append_to_ledger("FIND-001", {"trip_id": "T-1", "verdict": "DISCREPANCY", "amount": 26.00})
    assert e1["prev_hash"] == "0" * 64
    assert len(e1["event_hash"]) == 64

    e2 = append_to_ledger("FIND-002", {"trip_id": "T-2", "verdict": "MATCH", "amount": 0.00})
    assert e2["prev_hash"] == e1["event_hash"]

    # Step 2: Verify intact chain
    v_ok = verify_chain()
    assert v_ok["valid"] is True
    assert v_ok["total_blocks"] >= 2

    # Step 3: Tamper with event 1
    tamper_success = tamper_ledger_entry(e1["event_id"], {"trip_id": "T-1", "verdict": "DISCREPANCY", "amount": 9999.00})
    assert tamper_success is True

    # Step 4: Verification must fail
    v_tampered = verify_chain()
    assert v_tampered["valid"] is False
    assert v_tampered["broken_at_event_id"] == e1["event_id"]
