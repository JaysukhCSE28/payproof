"use client";

import React from "react";

interface Props {
  claimedFare: string;
  computedFare?: string | null;
  difference?: string | null;
  tolerance?: string;
}

export const AmountCards: React.FC<Props> = ({
  claimedFare,
  computedFare,
  difference,
  tolerance = "1.00",
}) => {
  const diffNum = difference ? parseFloat(difference) : 0;
  const isDiscrepancy = Math.abs(diffNum) > parseFloat(tolerance);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-4">
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
        <p className="text-xs uppercase font-mono tracking-wider text-slate-400">Claimed Paid Amount</p>
        <p className="text-2xl font-bold font-mono text-white mt-1">₹{claimedFare}</p>
        <p className="text-xs text-slate-500 mt-1">From driver trip evidence</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
        <p className="text-xs uppercase font-mono tracking-wider text-slate-400">Deterministic Expected Fare</p>
        <p className="text-2xl font-bold font-mono text-emerald-400 mt-1">
          {computedFare ? `₹${computedFare}` : "N/A (Abstained)"}
        </p>
        <p className="text-xs text-slate-500 mt-1">Python Decimal Math Sandbox</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
        <p className="text-xs uppercase font-mono tracking-wider text-slate-400">Net Difference</p>
        <p
          className={`text-2xl font-bold font-mono mt-1 ${
            isDiscrepancy ? "text-rose-400" : "text-emerald-400"
          }`}
        >
          {difference ? `₹${parseFloat(difference) > 0 ? "+" : ""}${difference}` : "N/A"}
        </p>
        <p className="text-xs text-slate-500 mt-1">Tolerance threshold: ±₹{tolerance}</p>
      </div>
    </div>
  );
};
