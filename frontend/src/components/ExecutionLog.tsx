"use client";

import React from "react";

interface Props {
  log?: string[] | null;
}

export const ExecutionLog: React.FC<Props> = ({ log }) => {
  if (!log || log.length === 0) {
    return (
      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-slate-500 font-mono text-xs">
        No execution trace recorded.
      </div>
    );
  }

  return (
    <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
      <div className="flex justify-between items-center border-b border-slate-800 pb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          Live Execution Trace Log
        </span>
        <span className="text-[10px] font-mono text-slate-500">7-Step Deterministic Audit</span>
      </div>
      <div className="space-y-1 font-mono text-xs text-slate-300">
        {log.map((line, idx) => (
          <div key={idx} className="flex gap-2">
            <span className="text-slate-600 select-none">[{idx + 1}]</span>
            <span
              className={
                line.includes("DISCREPANCY")
                  ? "text-rose-400"
                  : line.includes("MATCH")
                  ? "text-emerald-400"
                  : line.includes("CANNOT_DETERMINE") || line.includes("ABSTAIN")
                  ? "text-amber-400"
                  : "text-slate-300"
              }
            >
              {line}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
