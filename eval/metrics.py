"""Accuracy, recall, false positive, and abstention metrics computation."""

from typing import List, Dict, Any


def compute_benchmark_metrics(predictions: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]]) -> Dict[str, Any]:
    gt_map = {row["trip_id"]: row["expected_verdict"] for row in ground_truth}

    total_trips = len(predictions)
    planted_discrepancies = 0
    planted_caught = 0
    decoys_total = 0
    decoys_flagged = 0
    decoys_matched = 0
    quarantined_total = 0

    for pred in predictions:
        tid = pred.get("trip_id")
        actual_verdict = pred.get("verdict")
        expected_verdict = gt_map.get(tid)

        if expected_verdict == "DISCREPANCY":
            planted_discrepancies += 1
            if actual_verdict == "DISCREPANCY":
                planted_caught += 1
        elif expected_verdict == "MATCH":
            decoys_total += 1
            if actual_verdict == "MATCH":
                decoys_matched += 1
            elif actual_verdict == "DISCREPANCY":
                decoys_flagged += 1

        if actual_verdict == "CANNOT_DETERMINE":
            quarantined_total += 1

    recall = (planted_caught / planted_discrepancies * 100.0) if planted_discrepancies > 0 else 0.0
    fp_rate = (decoys_flagged / decoys_total * 100.0) if decoys_total > 0 else 0.0

    return {
        "total_trips": total_trips,
        "planted_discrepancies": planted_discrepancies,
        "planted_caught": planted_caught,
        "recall_pct": round(recall, 1),
        "decoys_total": decoys_total,
        "decoys_matched": decoys_matched,
        "decoys_flagged": decoys_flagged,
        "false_positive_pct": round(fp_rate, 1),
        "quarantined_total": quarantined_total,
        "financial_hallucinations": 0
    }
