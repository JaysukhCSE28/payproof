"use client";

import React from "react";

interface Props {
  breakdown?: Record<string, any> | null;
}

export const CalcBreakdown: React.FC<Props> = ({ breakdown }) => {
  if (!breakdown) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-slate-400 text-sm italic">
        No arithmetic breakdown available (trip abstained or uncomputed).
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-4">
      <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
        Deterministic Formula Trace
      </h3>
      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 font-mono text-xs text-slate-300 space-y-1">
        <p className="text-emerald-400">
          Expected = Base (₹{breakdown.base_fare_inr}) + Distance ({breakdown.distance_km}km × ₹{breakdown.per_km_inr} × {breakdown.vehicle_multiplier}x) + Surcharges + Toll/Parking
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800">
          <span className="text-slate-500 block">Base Pay</span>
          <span className="text-slate-200 font-bold">₹{breakdown.base_fare_inr}</span>
        </div>
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800">
          <span className="text-slate-500 block">Distance Pay</span>
          <span className="text-slate-200 font-bold">₹{breakdown.distance_fare_inr}</span>
        </div>
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800">
          <span className="text-slate-500 block">Night Extra (1.25x)</span>
          <span className="text-slate-200 font-bold">₹{breakdown.night_extra_inr || "0.00"}</span>
        </div>
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800">
          <span className="text-slate-500 block">Toll / Parking</span>
          <span className="text-slate-200 font-bold">₹{breakdown.allowed_toll_inr || "0.00"}</span>
        </div>
      </div>
    </div>
  );
};
