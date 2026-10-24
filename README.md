# PayProof

Local-first trip-claim auditor. Policy retrieval feeds **reviewed rule cards**; dual calculation engines produce a verdict of `MATCH`, `DISCREPANCY`, or `CANNOT_DETERMINE`. Approved findings append to a hash-chained ledger.

## Stack

- Backend: FastAPI (`backend/`)
- Frontend: Next.js App Router (`frontend/`)
- Contracts: JSON Schema (`contracts/`)
- Eval: synthetic trips + metrics (`eval/`)

## Quick start

```bash
cp .env.example .env
make setup
make run
```

PowerShell (Windows, if `make` is unavailable):

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd frontend; npm install; cd ..
python scripts/seed_db.py
```

Then start the API (`uvicorn backend.app.main:app --reload --app-dir .`) and the UI (`npm run dev` in `frontend/`).

## Layout

See the repository tree: `contracts/`, `data/`, `backend/`, `frontend/`, `eval/`, `scripts/`, `demo/`.

## Limitations (scaffold)

Application logic is not implemented yet. Database file `data/payproof.db` is generated locally and gitignored.
