"""Abstention rules for ambiguous or injected inputs."""


def must_abstain(payload: dict) -> bool:
    # TODO: return True on conflicting fields, injection markers, or low confidence
    raise NotImplementedError("must_abstain")
