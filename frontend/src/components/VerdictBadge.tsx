"use client";

import React from "react";
import { Verdict } from "../lib/types";

interface Props {
  verdict: Verdict;
}

export const VerdictBadge: React.FC<Props> = ({ verdict }) => {
  if (verdict === "MATCH") {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
        ✓ MATCH (≤ ₹1.00)
      </span>
    );
  }
  if (verdict === "DISCREPANCY") {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
        ⚠ DISCREPANCY (&gt; ₹1.00)
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
      ? CANNOT_DETERMINE
    </span>
  );
};
