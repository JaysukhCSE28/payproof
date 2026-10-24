"""Safe tamper-detection demonstration script."""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.db import get_connection, init_schema
from backend.app.ledger.chain import append_to_ledger, verify_chain, tamper_ledger_entry


def run_tamper_demo() -> None:
    print("=== TAMPER-EVIDENT LEDGER DEMONSTRATION ===")
    conn = get_connection()
    init_schema(conn)
    conn.close()

    # Step 1: Append two valid blocks
    print("\n1. Appending Block 1 (Finding FIND-DEMO-01)...")
    b1 = append_to_ledger("FIND-DEMO-01", {"trip_id": "TRIP-1001", "expected": 53.00, "paid": 42.00})
    print(f"   Block 1 Hash: {b1['event_hash']}")

    print("\n2. Appending Block 2 (Finding FIND-DEMO-02)...")
    b2 = append_to_ledger("FIND-DEMO-02", {"trip_id": "TRIP-1002", "expected": 57.00, "paid": 45.00})
    print(f"   Block 2 Hash: {b2['event_hash']}")

    # Step 3: Verify initial chain
    print("\n3. Verifying initial chain status...")
    v1 = verify_chain()
    print(f"   Chain status: {v1['message']} (Valid: {v1['valid']})")

    # Step 4: Deliberately tamper with Block 1 payload
    print(f"\n4. Simulating database tampering on {b1['event_id']} (modifying paid amount from 42.00 to 53.00)...")
    tamper_ledger_entry(b1['event_id'], {"trip_id": "TRIP-1001", "expected": 53.00, "paid": 53.00})
    print("   Database row modified directly.")

    # Step 5: Verify chain after tampering
    print("\n5. Re-running chain verification...")
    v2 = verify_chain()
    print(f"   Chain status: Valid={v2['valid']}")
    if not v2['valid']:
        print(f"   SUCCESSFULLY CAUGHT CORRUPTION: {v2['reason']}")
    print("\n=== DEMONSTRATION COMPLETE ===")


if __name__ == "__main__":
    run_tamper_demo()
