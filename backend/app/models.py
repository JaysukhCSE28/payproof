"""Pydantic models matching contracts/ JSON Schema."""

from typing import Literal

from pydantic import BaseModel

Verdict = Literal["MATCH", "DISCREPANCY", "CANNOT_DETERMINE"]


class Trip(BaseModel):
    trip_id: str
    # TODO: align remaining fields with contracts/trip.schema.json


class RuleCard(BaseModel):
    rule_id: str
    version: int
    status: Literal["reviewed"] = "reviewed"
    # TODO: align remaining fields with contracts/rule_card.schema.json


class Finding(BaseModel):
    finding_id: str
    trip_id: str
    verdict: Verdict
    # TODO: align remaining fields with contracts/finding.schema.json


class LedgerEvent(BaseModel):
    event_id: str
    finding_id: str
    prev_hash: str
    event_hash: str
    payload: dict
    # TODO: align remaining fields with contracts/ledger_event.schema.json
