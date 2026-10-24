"""GET /ledger, GET /ledger/verify."""

from typing import List, Dict, Any
from fastapi import APIRouter
from backend.app.ledger.chain import list_ledger_events, verify_chain

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("")
def get_ledger() -> List[Dict[str, Any]]:
    """Return all append-only tamper-evident ledger events."""
    return list_ledger_events()


@router.get("/verify")
def verify_ledger() -> Dict[str, Any]:
    """Recompute all block hashes and report ledger chain cryptographic integrity."""
    return verify_chain()
