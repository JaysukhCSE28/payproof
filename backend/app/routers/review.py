"""POST /review/{finding_id}/approve, /reject."""

from fastapi import APIRouter

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/{finding_id}/approve")
def approve_finding(finding_id: str) -> dict[str, str]:
    # TODO: append approved finding to the hash-chained ledger
    raise NotImplementedError("approve_finding")


@router.post("/{finding_id}/reject")
def reject_finding(finding_id: str) -> dict[str, str]:
    # TODO: record rejection without writing a ledger event
    raise NotImplementedError("reject_finding")
