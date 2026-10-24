"""Prototype canonical JSON serializer.

Note: Clearly labeled as a prototype canonicalizer enforcing lexicographical key sorting,
compact separators (no whitespace), and UTF-8 encoding. It does not claim full RFC 8785 compliance.
"""

import json
from typing import Any


def canonicalize(data: Any) -> str:
    """Serialize data into a deterministic, sorted-key compact JSON string."""
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def canonicalize_bytes(data: Any) -> bytes:
    """Return UTF-8 encoded bytes of canonicalized JSON."""
    return canonicalize(data).encode("utf-8")
