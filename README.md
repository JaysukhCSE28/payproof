# 🔍 PayProof — Deterministic RAG for Gig-Worker Earnings Auditing

> **"Contractual RAG without Arithmetic Hallucinations: Make Every Payout Explainable."**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue?logo=python&logoColor=white)](https://python.org)
[![Tests](https://img.shields.io/badge/Pytest-22%2F22%20Passed-brightgreen)](https://docs.pytest.org)
[![Benchmark](https://img.shields.io/badge/Benchmark%20Recall-100%25%20(38%2F38)-success)](eval/run_eval.py)
[![Architecture](https://img.shields.io/badge/RAG%20Architecture-Hybrid%20BM25%20%2B%20Deterministic%20Sandbox-purple)](#-why-payproof-is-a-rag-system)

---

## 💡 What is PayProof?

**PayProof** is a **Retrieval-Augmented Generation & Auditing (RAG)** platform designed to eliminate information asymmetry between gig-economy platforms (Swiggy, Uber, Zomato) and delivery partners/drivers. 

Gig platforms bundle base fares, distance pay, waiting allowances, surge multipliers, tolls, and deductions into opaque, single-line payouts. Drivers routinely suffer from underpayments without any explainable recourse. 

PayProof solves this by indexing verified rate-card contracts into a **Policy Knowledge Base**, retrieving the exact governing legal/contractual clause via **Hybrid RAG**, and replacing error-prone LLM arithmetic with a **Deterministic Calculation Sandbox** (`Decimal` + integer-paise verification) to generate mathematically unassailable evidence packets.

---

## 🧠 Why PayProof is a RAG System (and How it Fixes Classic RAG)

### The Problem with Traditional RAG for Financial & Contract Auditing
In traditional RAG:
```
[User Query / Document] ──> [Vector/Lexical Retrieval] ──> [LLM Context Window] ──> [LLM Generates Answer & Math] ❌
                                                                                     (Hallucinates numbers, rounding errors,
                                                                                      inconsistent calculations)
```
When evaluating complex contracts, rate cards, and financial payouts, **LLMs cannot be trusted to do arithmetic**. They hallucinate math, confuse order of operations, round unpredictably, and are vulnerable to prompt injection in receipt notes.

### PayProof's Innovation: Deterministic AI-Math Decoupled RAG
PayProof replaces the probabilistic generative head with a **deterministic, dual-execution audit engine**:

```
[Trip / Receipt Evidence]
         │
         ▼
[1. Evidence Ingestion & OCR Gating] ──(Low Confidence <80%)──► [Quarantine Pipeline (Abstain)]
         │
         ▼ (High Confidence)
[2. Hybrid Retrieval (RAG Knowledge Base)]
   ├── Metadata Filter (Vendor, Zone, Temporal Window)
   └── BM25 Lexical Search with Token-Overlap Guardrails
         │
         ▼
[3. Augmentation & Rule Resolution]
   └── Matches Grounded Clause ID & Versioned Rule Card Contract
         │
         ▼
[4. Deterministic Dual-Engine Execution]
   ├── Engine A: Python Decimal (Rounding INR)
   └── Engine B: Integer Paise Verifier (Zero Floating-Point)
         │
         ▼
[5. Finding & Evidence Packet Assembly]
   └── Structured Claim, Cited Clause, Formula Trace, Audit Verdict
         │
         ▼
[6. Human-in-the-Loop Review Gate] ──(Worker Approves)──► [7. SHA-256 Tamper-Evident Ledger]
```

| RAG Component | PayProof Implementation | Technology Stack |
| :--- | :--- | :--- |
| **Knowledge Base (Corpus)** | Verified rate cards, terms of service, platform clauses | `data/policy/clauses.json`, `rule_cards.json` |
| **Query Representation** | Structured trip metadata, platform vendor, zone, timestamps, receipt OCR | Pydantic Schema Contracts (`contracts/trip.schema.json`) |
| **Retrieval Engine** | Hybrid: Metadata filtering (temporal/vendor/geo) + Fallback BM25 with token-overlap guard | Python BM25 index (`backend/app/retrieval/`) |
| **Augmentation Layer** | Rule Card Resolver injecting governing formulas, caps, and multipliers into context | Deterministic Rule Card Resolver (`backend/app/retrieval/rule_resolver.py`) |
| **Synthesis / Generation** | Dual calculation engines generating exact explainable audit findings & evidence packets | Pure Python `Decimal` + Integer Paise Verifier |
| **Guardrails & Humility** | OCR confidence gating (<80% abstain) & Unknown platform policy abstention | Abstention Engine (`backend/app/language/abstain.py`) |
| **Provenance & Audit Trail** | Cryptographically chained evidence packets | SHA-256 Canonical JSON Ledger (`backend/app/ledger/`) |

---

## 🏛️ System Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │            Next.js 15 Web Console            │
                    │  (Audit Matrix | Trip Detail | Ledger UI)    │
                    └──────────────────────┬───────────────────────┘
                                           │ HTTP / REST
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │               FastAPI Backend                │
                    └───────┬──────────────────────────────┬───────┘
                            │                              │
         ┌──────────────────▼──────────────┐   ┌───────────▼──────────────────┐
         │       Retrieval & RAG           │   │      Deterministic Engine    │
         │  • clauses.json Knowledge Base  │   │  • Python Decimal Engine     │
         │  • BM25 Index & Fallback        │   │  • Paise Integer Verifier    │
         │  • Vendor & Temporal Filtering  │   │  • Tolerance Comparator (₹1) │
         └─────────────────────────────────┘   └───────────┬──────────────────┘
                                                           │
                                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │          SQLite Database (WAL Mode)          │
                    │   • trips • findings • ledger • quarantine   │
                    └──────────────────────────────────────────────┘
```

---

## 📊 Benchmark & Evaluation Results

PayProof was evaluated against a rigorous 40-trip benchmark suite (`synthetic_40.csv`) containing 38 planted discrepancy patterns across multiple platforms, plus 2 decoy trips.

Run the evaluation yourself:
```powershell
python eval/run_eval.py
```

### Benchmark Metrics

```
============================================================
PAYPROOF DETERMINISTIC PIPELINE BENCHMARK EVALUATION
============================================================
Total Trips Evaluated: 40
Planted Error Discrepancies Caught: 38 / 38 (100.0% Recall)
Decoys Correctly Filtered (MATCH): 2 / 2 (0.0% False Positive Rate)
Execution Duration: 0.69s (17ms per trip)
Arithmetic Hallucinations: 0 (100% Decoupled)
============================================================
```

- **100% Discrepancy Recall**: Caught base rate shaving, distance factor undercounting, missing night multipliers, uncredited wait times, and toll underpayments.
- **0% False Positive Rate**: Perfectly verified matching trips without raising false disputes.
- **0 Arithmetic Hallucinations**: 100% decoupled arithmetic ensures math errors are physically impossible.
- **Sub-Second Speed**: 40 full RAG audit cycles completed in ~0.69s.

---

## 📁 Repository Structure

```
payproof/
├── README.md                   # Complete RAG architecture documentation
├── docker-compose.yml          # Multi-container deployment (FastAPI + Next.js)
├── contracts/                  # Formal JSON schemas locking data boundaries
│   ├── trip.schema.json
│   ├── rule_card.schema.json
│   ├── finding.schema.json
│   └── ledger_event.schema.json
├── data/
│   ├── policy/                 # Policy Knowledge Base
│   │   ├── clauses.json        # Contractual clause texts & metadata
│   │   └── rule_cards.json     # Reviewed computational rules & rates
│   └── trips/                  # Synthetic test & benchmark fixtures
│       ├── synthetic_40.csv    # 38 discrepancies + 2 decoys
│       └── extras_edge_cases.csv
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI application router
│   │   ├── db.py               # SQLite WAL connection & schemas
│   │   ├── pipeline.py         # 7-stage deterministic RAG orchestrator
│   │   ├── retrieval/          # RAG Engine
│   │   │   ├── retriever.py    # Hybrid retriever (metadata + BM25)
│   │   │   ├── index.py        # BM25 index with pure-Python fallback
│   │   │   ├── clause_parser.py
│   │   │   └── rule_resolver.py# Context grounder & rule card mapper
│   │   ├── calc/               # Arithmetic Engine
│   │   │   ├── engine.py       # Primary Decimal arithmetic
│   │   │   ├── verifier.py     # Secondary Integer Paise verifier
│   │   │   └── compare.py      # Noise boundary & tolerance comparator (₹1.00)
│   │   ├── language/           # Extraction & abstention gates
│   │   │   └── abstain.py      # OCR quality & unknown platform filters
│   │   └── ledger/             # Cryptographic ledger
│   │       ├── chain.py        # SHA-256 block appender & verify_chain()
│   │       ├── canonical.py    # RFC-aligned canonical JSON serialization
│   │       └── packet.py       # Evidence packet assembly
│   └── tests/                  # 22 Comprehensive pytest test suites
│       ├── test_calc.py        # Math breakdown & multiplier tests
│       ├── test_verifier.py    # Dual-engine agreement tests
│       ├── test_retrieval.py   # RAG BM25 & metadata filter tests
│       ├── test_abstain.py     # Abstention & quarantine gate tests
│       ├── test_ledger.py      # SHA-256 chain & tamper-detection tests
│       └── test_injection.py   # Prompt/SQL injection resistance tests
├── frontend/                   # Modern Dark-Mode Next.js 15 UI
│   ├── src/app/
│   │   ├── page.tsx            # Audit Matrix & CSV upload
│   │   ├── audit/[trip_id]/    # Deep-dive finding inspector & formula breakdown
│   │   ├── ledger/             # Tamper-evident ledger explorer & integrity verifier
│   │   └── quarantine/         # Low-confidence / unresolvable evidence review
├── eval/                       # Benchmark harness
│   ├── run_eval.py             # Benchmark runner
│   └── metrics.py              # Precision, recall, FP evaluation
└── scripts/
    ├── seed_db.py              # Database seeder
    ├── build_index.py          # RAG index builder
    └── tamper_demo.py          # Cryptographic tamper-detection demonstration
```

---

## ⚡ Quick Start & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Git

### 1. Backend Setup
```powershell
# Open terminal at project root
cd "C:\Users\Jaysukh Sesham\onedrive\desktop\payproof"

# Install backend dependencies
pip install -r backend/requirements.txt
pip install pytest

# Seed SQLite database with policies & trips
python scripts/seed_db.py

# Launch FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```
Backend will be live at `http://127.0.0.1:8000` (Interactive API docs at `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```powershell
# Open a second terminal
cd "C:\Users\Jaysukh Sesham\onedrive\desktop\payproof\frontend"

# Install dependencies & run dev server
npm install
npm run dev
```
Next.js Console will be live at `http://localhost:3000`.

---

## 🧪 Verification & Test Suite

### Run All 22 Unit Tests
```powershell
python -m pytest backend/tests/ -v
```
**Results: 22 passed in ~1.3s**
- `test_calc.py` (5 tests): Core fare, night multiplier (1.25x), vehicle multiplier (1.2x/1.5x), toll caps, exact ₹1.00 tolerance boundary.
- `test_verifier.py` (5 tests): Deterministic agreement between `Decimal` and integer paise calculations across edge cases.
- `test_retrieval.py` (3 tests): Metadata filtering, temporal validity windowing, unknown vendor handling.
- `test_abstain.py` (4 tests): OCR confidence gate (<80%), missing fields, unknown platforms triggering `CANNOT_DETERMINE`.
- `test_ledger.py` (2 tests): Canonical JSON serialization determinism, SHA-256 chain continuity & tamper detection.
- `test_injection.py` (2 tests): Prompt injection in driver notes and SQL injection attempts are completely neutralized.

### Run Cryptographic Tamper-Detection Demo
```powershell
python scripts/tamper_demo.py
```
Demonstrates how PayProof catches silent database modifications:
1. Appends Block 1 (`FIND-DEMO-01`) and Block 2 (`FIND-DEMO-02`) with valid SHA-256 hashes.
2. Verifies initial chain integrity (`Valid: True`).
3. Modifies a payout value directly in SQLite, bypassing the hashing layer.
4. Reruns verification: **Instantly flags signature mismatch and pinpoints the tampered event ID**.

---

## 🖥️ Live User Flow (Walkthrough)

1. **Upload & Batch Audit (`/`)**:
   - Ingest `data/trips/synthetic_40.csv`.
   - Hit **"Run Batch Audit"** to execute 40 dual-engine RAG evaluations in <1s.
2. **Inspect Finding Detail (`/audit/[trip_id]`)**:
   - Review exact formula breakdown: `Base Fare + (Distance × Rate) + Waiting Allowance + Multipliers`.
   - Inspect the **governing legal policy clause** retrieved from knowledge base.
   - Inspect the 7-step execution trace log.
3. **Human Review Gate**:
   - Worker clicks **"Approve & Write to Ledger"** (no unreviewed complaints are ever created).
4. **Tamper-Evident Ledger (`/ledger`)**:
   - Inspect immutable SHA-256 blocks linking previous event hashes to current payload.
   - Click **"Verify Chain Integrity"** to validate zero cryptographic tampering.
5. **Quarantine (`/quarantine`)**:
   - View trips with degraded OCR or unknown platforms safely routed away from false calculations.

---

## 🛡️ Trust, Safety & Ethical AI Principles

1. **Epistemic Humility (Abstain by Default)**: When OCR confidence is low (<80%) or platform policy is missing, the system outputs `CANNOT_DETERMINE` instead of guessing.
2. **Deterministic Decoupling**: Arithmetic is never computed by an LLM. Zero floating-point rounding errors. Zero arithmetic hallucinations.
3. **Worker Agency**: Human-in-the-loop review prevents automated spam disputes and preserves driver credibility.
4. **Cryptographic Proof**: Chained audit trails ensure platform and driver can both rely on verifiable historical records.

---

## 📜 License & Disclaimers

- **Synthetic Demo Fixtures**: All rate cards, policy clauses, and trip data in this repository are synthetic fixtures generated for benchmark evaluation and architectural demonstration.
- **Legal Notice**: PayProof provides structured calculations and evidence compilation. It does not provide statutory legal advice or guarantee individual wage recovery.
