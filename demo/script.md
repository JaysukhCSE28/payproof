# PayProof Live Demonstration Script (6-Minute Walkthrough)

## Overview & Demo Sequence
This script provides the complete step-by-step narrative for demonstrating PayProof during hackathon judging.

---

### Minute 0:00 - 1:00: Problem Statement & Core Architectural Principle
- **Hook**: "Over 40% of Indian gig workers earn under ₹15,000/month. Their pay statements combine base rates, per-km fees, night multipliers, waiting charges, and platform fees into a single unitemized figure. Workers have no way to verify if they were underpaid."
- **The LLM Trap**: "If you ask a general-purpose LLM to audit payouts, it hallucinates arithmetic. In financial auditing, a 95% accurate model is completely unusable."
- **Our Innovation**: **Deterministic AI-Math Decoupling**.
  - AI parses documents and retrieves policy clauses.
  - 100% of arithmetic calculations execute in a sandboxed, isolated Python engine using `Decimal` and independent integer-paise verification.

---

### Minute 1:00 - 2:30: Ingestion & Batch Auditing Demo
- **Action**: Open the web application at `http://localhost:3000`.
- **Action**: Click **Select CSV Trip Batch** and select `data/trips/synthetic_40.csv`.
- **Talking Point**: "We ingest a batch of 40 trips. The system normalizes distances, dates, and claimed amounts, immediately displaying them in the Trip Audit Matrix."
- **Action**: Click **Run Batch Deterministic Audit**.
- **Talking Point**: "Watch the matrix update in real time. In under 15 seconds, the engine compares all 40 trips against applicable rate cards using exact metadata filtering and BM25 clause retrieval."

---

### Minute 2:30 - 3:45: Deep-Dive on Discrepancy Inspection
- **Action**: Filter matrix by `DISCREPANCY` and click **Inspect** on `TRIP-1001`.
- **Showcase**:
  1. **Amount Cards**: Claimed paid amount ₹42.00 vs Expected ₹53.00 (Delta: +₹11.00).
  2. **Deterministic Formula Trace**: Base (₹25.00) + Distance (3.5km × ₹8.00/km = ₹28.00) = ₹53.00.
  3. **Governing Policy Citation**: Displays the exact reviewed rate card (`RULE-SWIGGY-MAA-2026-V1`) and source reference.
  4. **Live Execution Trace**: 7-step deterministic log showing provenance, Decimal calculation, and paise verification agreement.

---

### Minute 3:45 - 4:45: Human Review Gate & Tamper-Evident Ledger
- **Talking Point**: "PayProof has a strict **Human-in-the-Loop Gate**. The agent never files complaints autonomously to platforms. Only when a worker reviews the evidence and explicitly clicks Approve is a record written to the ledger."
- **Action**: Click **Approve & Write to Ledger**.
- **Action**: Navigate to `http://localhost:3000/ledger`.
- **Showcase**:
  - Show the newly appended block with its previous block hash and newly minted SHA-256 hash.
  - Explain: "Each block contains canonical JSON of the finding. It is tamper-evident."
- **Action**: Click **Verify Chain Cryptographic Integrity**.
  - Show green badge: `✓ LEDGER CHAIN INTACT (100% VALID)`.

---

### Minute 4:45 - 5:30: Tamper Detection Demonstration
- **Action**: Run terminal command: `python scripts/tamper_demo.py` (or demonstrate in UI).
- **Talking Point**: "What happens if someone modifies a record in the database? Let's alter a record's paid amount."
- **Action**: Click **Verify Chain Cryptographic Integrity** again.
- **Showcase**:
  - Show red banner: `⚠ TAMPER CORRUPTION DETECTED - Hash signature invalid`.
  - "The cryptographic chain immediately flags the alteration, preventing any fabricated evidence from being passed off as original."

---

### Minute 5:30 - 6:00: Epistemic Humility & Conclusion
- **Action**: Navigate to `/quarantine`.
- **Talking Point**: "When receipt images have OCR confidence below 80% or policy terms are ambiguous, PayProof doesn't guess. It abstains with `CANNOT_DETERMINE` and routes to Quarantine."
- **Closing**: "Autonomous interpretation. Deterministic calculation. Human control. Every payout deserves a provable explanation. Thank you."
