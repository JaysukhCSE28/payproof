# Demo script

1. Copy `.env.example` to `.env` (leave API keys empty for offline mode).
2. Run `make setup` then `make seed`.
3. Start backend and frontend (`make run` or Docker Compose once images exist).
4. Upload `data/trips/synthetic_40.csv` on the home page.
5. Open a `DISCREPANCY` inspection, approve it, then verify the ledger.
6. Run `python scripts/tamper_demo.py` to show chain break detection.

TODO: fill timings and talking points once the pipeline is implemented.
