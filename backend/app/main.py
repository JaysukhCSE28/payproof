"""FastAPI entrypoint: CORS, schema initialization, and router mounts."""

import sys
from pathlib import Path

# Ensure project root is in sys.path so 'backend.app' can always be resolved
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db import get_connection, init_schema
from backend.app.config import settings
from backend.app.routers import ingest, audit, review, ledger

# Initialize database schema on module load
conn = get_connection()
init_schema(conn)
conn.close()

app = FastAPI(
    title="PayProof",
    description="Deterministic AI-Decoupled Auditing Engine for Gig-Worker Earnings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", settings.frontend_origin, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "system": "PayProof Deterministic Engine",
        "version": "1.0.0",
        "amount_tolerance_inr": settings.amount_tolerance_inr,
        "ocr_min_confidence": settings.ocr_min_confidence
    }


# Mount API routers
app.include_router(ingest.router)
app.include_router(audit.router)
app.include_router(review.router)
app.include_router(ledger.router)
