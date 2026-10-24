"""Quarantine router for low-confidence or incomplete records."""


def should_quarantine(record: dict) -> bool:
    # TODO: quarantine on low OCR confidence or missing required fields
    raise NotImplementedError("should_quarantine")
