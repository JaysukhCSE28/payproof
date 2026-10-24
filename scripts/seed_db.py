"""Database and fixture seeder script."""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
from backend.app.db import get_connection, init_schema
from backend.app.evidence.csv_loader import load_trips_csv
from eval.generate_dataset import generate_datasets


def seed_database() -> None:
    print("Step 1: Generating synthetic datasets...")
    generate_datasets(str(PROJECT_ROOT / "data" / "trips"))

    print("Step 2: Initializing SQLite schema...")
    conn = get_connection()
    init_schema(conn)
    cursor = conn.cursor()

    print("Step 3: Seeding policy clauses...")
    clauses_file = PROJECT_ROOT / "data" / "policy" / "clauses.json"
    if clauses_file.exists():
        clauses = json.loads(clauses_file.read_text(encoding="utf-8"))
        for c in clauses:
            cursor.execute("""
            INSERT OR REPLACE INTO clauses (
                clause_id, text, platform_vendor, zone, effective_from, effective_to, source_reference, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["clause_id"], c["text"], c["platform_vendor"], c["zone"],
                c.get("effective_from"), c.get("effective_to"), c.get("source_reference"),
                json.dumps(c.get("tags", []))
            ))
        print(f"  Loaded {len(clauses)} policy clauses.")

    print("Step 4: Seeding reviewed rule cards...")
    rules_file = PROJECT_ROOT / "data" / "policy" / "rule_cards.json"
    if rules_file.exists():
        rule_cards = json.loads(rules_file.read_text(encoding="utf-8"))
        for r in rule_cards:
            cursor.execute("""
            INSERT OR REPLACE INTO rule_cards (
                rule_id, version, status, clause_id, zone, trip_type, effective_from, effective_to, formula_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r["rule_id"], r["version"], r["status"], r["clause_id"],
                r.get("zone"), r.get("trip_type"), r.get("effective_from"),
                r.get("effective_to"), json.dumps(r.get("formula", {}))
            ))
        print(f"  Loaded {len(rule_cards)} reviewed rule cards.")

    print("Step 5: Seeding synthetic_40 trips...")
    trips_csv = PROJECT_ROOT / "data" / "trips" / "synthetic_40.csv"
    if trips_csv.exists():
        trips = load_trips_csv(trips_csv)
        for t in trips:
            cursor.execute("""
            INSERT OR REPLACE INTO trips (
                trip_id, employee_id, occurred_at, zone, city, vendor, vehicle_type, trip_type,
                distance_km, claimed_fare_inr, claimed_toll_inr, claimed_parking_inr, claimed_wait_inr,
                wait_minutes, is_night, ocr_confidence, ocr_text, notes, planted_error, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["trip_id"], t["employee_id"], t["occurred_at"], t["zone"], t["city"],
                t["vendor"], t["vehicle_type"], t["trip_type"], t["distance_km"],
                t["claimed_fare_inr"], t["claimed_toll_inr"], t["claimed_parking_inr"],
                t["claimed_wait_inr"], t["wait_minutes"], 1 if t["is_night"] else 0,
                t["ocr_confidence"], t["ocr_text"], t["notes"], t["planted_error"],
                json.dumps(t)
            ))
        print(f"  Loaded {len(trips)} trips into database.")

    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
