"""Prototype canonical JSON serializer for hashing.

Stable key order and UTF-8 encoding only. Not a standardized canonical JSON profile.
"""


def dumps_canonical(payload: dict) -> bytes:
    # TODO: sort keys, no insignificant whitespace, encode utf-8
    raise NotImplementedError("dumps_canonical")
