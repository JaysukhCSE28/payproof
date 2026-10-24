"""Dual-engine comparison and INR 1.00 tolerance logic."""

from decimal import Decimal

from backend.app.models import Verdict


def compare_amounts(claimed: Decimal, computed: Decimal, verified_paise: int) -> Verdict:
    # TODO: engines must agree; then apply AMOUNT_TOLERANCE_INR (default 1.00)
    # Disagree or insufficient data -> CANNOT_DETERMINE
    raise NotImplementedError("compare_amounts")
