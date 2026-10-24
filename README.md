# PayProof — Autonomous Deterministic Gig-Worker Earnings Auditor

> **"Make every payout explainable."**

PayProof is an autonomous, deterministic auditing agent built to resolve information asymmetry between gig-economy platforms (e.g., Swiggy, Uber, Zomato) and gig workers. Gig platforms bundle base pay, distance, duration, night multipliers, waiting time, and deductions into an unitemized total. PayProof reconstructs the governing rate cards, recomputes expected pay using sandboxed Python arithmetic, filters noise (≤ ₹1.00), abstains from low-confidence evidence (< 80%), requires human approval before filing, and records verified findings to a tamper-evident, SHA-256 hash-chained ledger.

---

## 🏛️ Core Architectural Principle: Deterministic AI-Math Decoupling

| Layer | Responsibility | Technology | Math Behavior |
| :--- | :--- | :--- | :--- |
| **Language & Extraction** | OCR parsing, field extraction, intent classification | Gemini 2.5 Flash / Tesseract | **Strictly forbidden from computing arithmetic** |
| **Retrieval & RAG** | Fetch governing policy clauses by platform, zone, and date | BM25 + Metadata Filtering | Evidence citation only; not executable code |
| **Deterministic Audit Sandbox** | Compute expected payout and discrepancy | Pure Python `Decimal` + Paise Verifier | 100% exact math; zero floating-point error |
| **Human Review Gate** | Worker inspects evidence, formula, and delta before approval | Next.js UI | No autonomous complaint submissions |
| **Integrity Ledger** | Immutable cryptographic chain of approved findings | Prototype Canonical JSON + SHA-256 | Tamper-evident proof of audit state |

---

## 📁 Repository Structure

```
payproof/
├── README.md                   # Complete system documentation
├── docker-compose.yml          # Multi-container orchestration (Backend + Frontend)
├── .env.example                # Configuration & API keys
├── Makefile                    # Developer task automation
├── contracts/                  # JSON Schemas locking data contracts
│   ├── trip.schema.json
│   ├── rule_card.schema.json
│   ├── finding.schema.json
│   └── ledger_event.schema.json
├── data/
│   ├── policy/                 # Reviewed rule cards and clause text
│   │   ├── clauses.json
│   │   └── rule_cards.json
│   └── trips/                  # Synthetic evaluation test suites
│       ├── synthetic_40.csv    # 38 planted discrepancies + 2 decoys
│       ├── ground_truth.csv    # Benchmark expected verdicts
│       └── extras_edge_cases.csv # ₹1.00 boundary, degraded OCR, missing fields
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint, CORS, router mounts
│   │   ├── config.py           # Environment settings & thresholds
│   │   ├── models.py           # Pydantic schemas matching /contracts
│   │   ├── db.py               # SQLite connection & schema initialization
│   │   ├── routers/            # API endpoints: /ingest, /audit, /review, /ledger
│   │   ├── evidence/           # CSV loader, OCR evaluator, normalizer, quarantine
│   │   ├── language/           # Prompt templates, extraction, abstention rules
│   │   ├── retrieval/          # Clause parser, BM25 index, hybrid retriever, rule resolver
│   │   ├── calc/               # Primary Decimal engine, Paise verifier, tolerance comparator
│   │   ├── ledger/             # Canonical serializer, SHA-256 chain, evidence packet builder
│   │   └── pipeline.py         # 7-stage deterministic orchestrator
│   └── tests/                  # 6 comprehensive pytest suites
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── app/                # Next.js App Router pages (Matrix, Detail, Ledger, Quarantine, Results)
│       ├── components/         # Reusable dark-mode UI components
│       └── lib/                # Typed API client & contracts interfaces
├── eval/
│   ├── generate_dataset.py     # Deterministic 40-trip generator
│   ├── metrics.py              # Recall, false-positive, and abstention metrics
│   └── run_eval.py             # Benchmark runner
├── scripts/
│   ├── seed_db.py              # Seeds SQLite with policies and 40 trips
│   ├── build_index.py          # BM25 index refresher
│   └── tamper_demo.py          # Demonstrates cryptographic chain break detection
└── demo/
    ├── script.md               # 6-minute live presentation script
    └── judge_qa.md             # Evidence-based answers to judge inquiries
```

---

## ⚡ Quick Start & Setup

### 1. Configure Environment
```bash
cp .env.example .env
```

### 2. Python Backend Setup (PowerShell / Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python scripts/seed_db.py
uvicorn backend.app.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 3. Next.js Frontend Setup (In a separate terminal)
```bash
cd frontend
npm install
npm run dev
```
Frontend Dashboard will be live at `http://localhost:3000`.

### 4. Running via Docker Compose
```bash
docker compose up --build
```

---

## 🧪 Running Tests & Benchmark Evaluation

### Run Backend Unit & Integration Tests:
```bash
python -m pytest backend/tests/ -v
```
Test Coverage:
1. `test_calc.py`: Formula breakdown, night multipliers, vehicle types, exact ₹1.00 boundary, ₹1.01 boundary.
2. `test_verifier.py`: Agreement between `Decimal` engine and integer paise engine.
3. `test_retrieval.py`: Metadata matching, temporal window validation, BM25 fallback.
4. `test_abstain.py`: Low OCR (< 80%), missing fields, unknown platforms triggering `CANNOT_DETERMINE`.
5. `test_ledger.py`: Append operations, hash continuity, tamper detection.
6. `test_injection.py`: Resistance to adversarial prompt injections in driver notes/OCR text.

### Run Synthetic 40-Trip Benchmark:
```bash
python eval/run_eval.py
```
Expected Output:
```
============================================================
PAYPROOF DETERMINISTIC PIPELINE BENCHMARK EVALUATION
============================================================
Total Trips Evaluated: 40
Planted Error Discrepancies Caught: 38 / 38 (100.0% Recall)
Decoys Correctly Filtered (MATCH): 2 / 2 (0.0% False Positive Rate)
Arithmetic Hallucinations: 0 (100% Decoupled)
============================================================
```

### Run Tamper-Detection Demonstration:
```bash
python scripts/tamper_demo.py
```

---

## ⚖️ Honest Disclaimers & Limitations
1. **Synthetic Demo Fixtures**: All rate cards, policy clauses, and trip logs in this prototype are synthetic fixtures designed to demonstrate algorithmic correctness. They do not represent proprietary platform secrets or certified live contracts.
2. **Prototype Canonical JSON**: JSON canonicalization implements sorted keys and compact separators. It is labeled as a prototype canonicalizer and does not claim full RFC 8785 float serialization compliance.
3. **Legal Disclaimer**: PayProof provides structured calculations to support evidence review. It does not guarantee wage recovery, constitute statutory legal representation, or establish that an employer violated labor laws.
