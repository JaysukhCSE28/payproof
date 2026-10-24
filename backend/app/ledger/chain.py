"""SHA-256 append and chain verifier."""


def append_event(payload: dict, prev_hash: str) -> dict:
    # TODO: hash canonical payload + prev_hash; persist ledger row
    raise NotImplementedError("append_event")


def verify_chain(events: list[dict]) -> bool:
    # TODO: recompute hashes; return False on tamper
    raise NotImplementedError("verify_chain")
