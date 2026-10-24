"""POST /ingest/trips, /screenshot, /policy."""

from fastapi import APIRouter

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/trips")
def ingest_trips() -> dict[str, str]:
    # TODO: accept CSV upload, validate against trip schema, persist
    raise NotImplementedError("ingest_trips")


@router.post("/screenshot")
def ingest_screenshot() -> dict[str, str]:
    # TODO: run OCR, quarantine low-confidence captures
    raise NotImplementedError("ingest_screenshot")


@router.post("/policy")
def ingest_policy() -> dict[str, str]:
    # TODO: store raw policy text for clause parsing
    raise NotImplementedError("ingest_policy")
