"""Build and test BM25 retrieval index on clauses."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.retrieval.clause_parser import load_clauses
from backend.app.retrieval.index import ClauseIndex


def main():
    clauses = load_clauses(str(PROJECT_ROOT / "data" / "policy" / "clauses.json"))
    print(f"Loaded {len(clauses)} clauses.")
    index = ClauseIndex(clauses)
    results = index.search("Swiggy Chennai rain surge night", top_k=2)
    print(f"BM25 Search found {len(results)} matches:")
    for r in results:
        print(f"  - [{r.get('clause_id')}] {r.get('text')[:80]}...")


if __name__ == "__main__":
    main()
