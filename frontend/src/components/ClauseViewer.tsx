"use client";

import React from "react";

interface Props {
  clauseId?: string | null;
  ruleId?: string | null;
  citation?: string | null;
}

export const ClauseViewer: React.FC<Props> = ({ clauseId, ruleId, citation }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
      <div className="flex justify-between items-center border-b border-slate-800 pb-2">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
          Governing Policy & Provenance
        </h3>
        <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          Verified Policy Fixture
        </span>
      </div>

      <div className="space-y-2 text-xs">
        <div>
          <span className="text-slate-500 block">Matched Clause ID</span>
          <span className="font-mono text-slate-200">{clauseId || "None (Default Fallback)"}</span>
        </div>
        <div>
          <span className="text-slate-500 block">Reviewed Rule Card</span>
          <span className="font-mono text-indigo-400">{ruleId || "None"}</span>
        </div>
        <div>
          <span className="text-slate-500 block">Source Reference</span>
          <p className="text-slate-300 italic mt-0.5">
            {citation || "Synthetic Demo Rate Card: Swiggy Chennai METRO v2.1"}
          </p>
        </div>
      </div>
    </div>
  );
};
