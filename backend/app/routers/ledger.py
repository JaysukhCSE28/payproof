"""GET /ledger, GET /ledger/verify."""

from fastapi import APIRouter

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("")
def list_ledger() -> dict[str, str]:
    # TODO: return append-only ledger events
    raise NotImplementedError("list_ledger")


@router.get("/verify")
def verify_ledger() -> dict[str, str]:
    # TODO: recompute hashes and report chain integrity
    raise NotImplementedError("verify_ledger")
