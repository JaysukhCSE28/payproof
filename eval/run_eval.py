"""Runs the actual audit pipeline over synthetic_40.csv against ground truth."""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import csv
import json
import time
from backend.app.db import get_connection, init_schema
from backend.app.evidence.csv_loader import load_trips_csv
from backend.app.pipeline import run_audit
from eval.metrics import compute_benchmark_metrics


def run_benchmark() -> dict:
    conn = get_connection()
    init_schema(conn)
    conn.close()

    trips_path = PROJECT_ROOT / "data" / "trips" / "synthetic_40.csv"
    gt_path = PROJECT_ROOT / "data" / "trips" / "ground_truth.csv"

    if not trips_path.exists() or not gt_path.exists():
        from eval.generate_dataset import generate_datasets
        generate_datasets(str(PROJECT_ROOT / "data" / "trips"))

    trips = load_trips_csv(trips_path)
    with open(gt_path, "r", encoding="utf-8") as f:
        ground_truth = list(csv.DictReader(f))

    print("============================================================")
    print("PAYPROOF DETERMINISTIC PIPELINE BENCHMARK EVALUATION")
    print("============================================================")
    print(f"Auditing {len(trips)} trips through isolated Python arithmetic sandbox...")

    start_time = time.time()
    predictions = []
    for t in trips:
        finding = run_audit(t["trip_id"], trip_data=t)
        predictions.append(finding.model_dump())

    elapsed = time.time() - start_time
    metrics = compute_benchmark_metrics(predictions, ground_truth)
    metrics["runtime_seconds"] = round(elapsed, 2)

    print(f"Total Trips Evaluated: {metrics['total_trips']}")
    print(f"Planted Error Discrepancies Caught: {metrics['planted_caught']} / {metrics['planted_discrepancies']} ({metrics['recall_pct']}%)")
    print(f"Decoys Correctly Filtered (MATCH): {metrics['decoys_matched']} / {metrics['decoys_total']} (FP Rate: {metrics['false_positive_pct']}%)")
    print(f"Execution Duration: {metrics['runtime_seconds']}s")
    print(f"Arithmetic Hallucinations: {metrics['financial_hallucinations']} (100% Decoupled)")
    print("============================================================")

    res_dir = PROJECT_ROOT / "eval" / "results"
    res_dir.mkdir(parents=True, exist_ok=True)
    (res_dir / "benchmark_report.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    run_benchmark()
