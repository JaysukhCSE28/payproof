"""Optional policy document ingestion tool (Firecrawl/Markdown/Text)."""

import json
from pathlib import Path
from backend.app.retrieval.clause_parser import parse_raw_policy_text


def ingest_policy_file(raw_file_path: str, vendor: str, zone: str, output_clauses_path: str = "data/policy/clauses.json"):
    p = Path(raw_file_path)
    if not p.exists():
        print(f"File {raw_file_path} not found.")
        return
    text = p.read_text(encoding="utf-8")
    new_clauses = parse_raw_policy_text(text, vendor, zone)
    out_p = Path(output_clauses_path)
    existing = []
    if out_p.exists():
        try:
            existing = json.loads(out_p.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    
    combined = existing + new_clauses
    out_p.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    print(f"Appended {len(new_clauses)} clauses to {output_clauses_path}.")


if __name__ == "__main__":
    print("Policy ingestion script ready.")
