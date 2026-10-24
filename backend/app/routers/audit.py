"""POST /audit/{trip_id}, /audit/batch."""

from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("/batch")
def audit_batch() -> dict[str, str]:
    # TODO: audit all eligible ingested trips
    # Declare /batch before /{trip_id} so "batch" is not captured as an id.
    raise NotImplementedError("audit_batch")


@router.post("/{trip_id}")
def audit_trip(trip_id: str) -> dict[str, str]:
    # TODO: call pipeline.run_audit and return finding
    raise NotImplementedError("audit_trip")
