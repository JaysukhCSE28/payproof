"""FastAPI entrypoint: CORS and router mounts."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO: import routers once implemented
# from backend.app.routers import ingest, audit, review, ledger

app = FastAPI(title="PayProof", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# TODO: app.include_router(ingest.router)
# TODO: app.include_router(audit.router)
# TODO: app.include_router(review.router)
# TODO: app.include_router(ledger.router)
