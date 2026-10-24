"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { listQuarantined } from "../../lib/api";

export default function QuarantinePage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    listQuarantined()
      .then(setItems)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <Link href="/" className="text-xs text-slate-400 hover:text-white flex items-center gap-1 font-mono">
            ← Back to Matrix
          </Link>
          <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            Epistemic Humility Gate
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-2">
          <h1 className="text-2xl font-bold text-white tracking-tight">Quarantined Inputs (CANNOT_DETERMINE)</h1>
          <p className="text-xs text-slate-400">
            PayProof abstains from calculating earnings when evidence is degraded, OCR confidence is below 80%, or governing policy terms are ambiguous.
          </p>
        </div>

        <div className="space-y-4">
          {loading ? (
            <div className="bg-slate-900 border border-slate-800 p-8 rounded-xl text-center text-slate-500 font-mono text-xs">
              Loading quarantined cases...
            </div>
          ) : items.length === 0 ? (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-xl text-center text-slate-500 italic text-sm">
              No quarantined inputs. All ingested trips have met required confidence thresholds.
            </div>
          ) : (
            items.map((q) => (
              <div
                key={q.id}
                className="bg-slate-900 border border-amber-500/30 p-5 rounded-xl space-y-3 font-mono text-xs"
              >
                <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                  <span className="text-amber-400 font-bold">Trip: {q.trip_id}</span>
                  <span className="text-slate-500 text-[11px]">{q.quarantined_at}</span>
                </div>

                <div className="space-y-1">
                  <span className="text-slate-400 block font-semibold">Abstention Reason:</span>
                  <p className="text-rose-300 bg-rose-950/30 p-2.5 rounded border border-rose-500/30 text-xs">
                    {q.reason}
                  </p>
                </div>

                {q.ocr_confidence !== null && (
                  <div className="text-[11px] text-slate-400">
                    <span>Recorded OCR Confidence: </span>
                    <span className="text-amber-400 font-bold">{q.ocr_confidence * 100}%</span>
                    <span className="text-slate-500"> (Required: &gt;= 80%)</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
