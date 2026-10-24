"""Dual-engine comparison and INR 1.00 tolerance logic."""

from decimal import Decimal
from typing import Tuple
from backend.app.models import Verdict
from backend.app.config import settings


def compare_amounts(claimed: Decimal, computed: Decimal, verified_paise: int) -> Tuple[Verdict, Decimal, str]:
    """
    1. Both engines (Decimal and integer-paise) must agree within rounding tolerance (1 paisa).
       If they diverge, abstain with CANNOT_DETERMINE.
    2. Apply AMOUNT_TOLERANCE_INR (default 1.00):
       - If abs(computed - claimed) <= 1.00: MATCH (noise filtered)
       - If abs(computed - claimed) > 1.00: DISCREPANCY
    Returns (verdict, difference, reason).
    """
    computed_paise = int(round(computed * 100))
    if abs(computed_paise - verified_paise) > 1:
        return (
            "CANNOT_DETERMINE",
            Decimal("0.00"),
            f"Arithmetic engine divergence: Decimal ({computed_paise}p) vs Paise ({verified_paise}p)"
        )

    difference = computed - claimed
    abs_diff = abs(difference)
    tolerance = Decimal(settings.amount_tolerance_inr)

    if abs_diff <= tolerance:
        verdict: Verdict = "MATCH"
        reason = f"Calculated fare ₹{computed:.2f} matches claimed fare ₹{claimed:.2f} within ₹{tolerance:.2f} tolerance."
    else:
        verdict = "DISCREPANCY"
        reason = f"Discrepancy detected: Calculated ₹{computed:.2f} vs Claimed ₹{claimed:.2f} (Delta: ₹{difference:+.2f})."

    return verdict, difference, reason
