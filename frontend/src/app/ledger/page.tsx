"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { listLedger, verifyLedger } from "../../lib/api";
import { LedgerEvent, LedgerVerificationResult } from "../../lib/types";

export default function LedgerPage() {
  const [events, setEvents] = useState<LedgerEvent[]>([]);
  const [verification, setVerification] = useState<LedgerVerificationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(false);

  const loadLedger = async () => {
    setLoading(true);
    try {
      const data = await listLedger();
      setEvents(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    setVerifying(true);
    try {
      const res = await verifyLedger();
      setVerification(res);
    } catch (err: any) {
      alert(`Verification failed: ${err.message}`);
    } finally {
      setVerifying(false);
    }
  };

  useEffect(() => {
    loadLedger();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <Link href="/" className="text-xs text-slate-400 hover:text-white flex items-center gap-1 font-mono">
            ← Back to Matrix
          </Link>
          <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            SHA-256 Hash Chained
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Tamper-Evident Audit Ledger</h1>
            <p className="text-xs text-slate-400 mt-1">
              Append-only sequential hash chain storing canonical JSON evidence packets of explicitly approved findings.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleVerify}
              disabled={verifying}
              className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-white text-xs font-bold transition flex items-center gap-2"
            >
              {verifying ? "Computing Hashes..." : "Verify Chain Cryptographic Integrity"}
            </button>
          </div>
        </div>

        {/* Verification banner */}
        {verification && (
          <div
            className={`p-4 rounded-xl border flex items-center justify-between text-xs font-mono ${
              verification.valid
                ? "bg-emerald-950/40 border-emerald-500/40 text-emerald-300"
                : "bg-rose-950/40 border-rose-500/40 text-rose-300"
            }`}
          >
            <div>
              <span className="font-bold block text-sm">
                {verification.valid ? "✓ LEDGER CHAIN INTACT (100% VALID)" : "⚠ TAMPER CORRUPTION DETECTED"}
              </span>
              <p className="mt-1">{verification.message || verification.reason}</p>
            </div>
            <span className="text-slate-400 font-sans">Checked {verification.total_blocks} blocks</span>
          </div>
        )}

        {/* Ledger Event List */}
        <div className="space-y-4">
          {loading ? (
            <div className="bg-slate-900 border border-slate-800 p-8 rounded-xl text-center text-slate-500 font-mono text-xs">
              Loading ledger blocks...
            </div>
          ) : events.length === 0 ? (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-xl text-center text-slate-500 italic text-sm">
              No approved findings committed to the ledger yet. Review and approve a discrepancy from the Trips Matrix.
            </div>
          ) : (
            events.map((evt, idx) => (
              <div
                key={evt.event_id}
                className="bg-slate-900 border border-slate-800 p-5 rounded-xl font-mono text-xs space-y-3 hover:border-slate-700 transition"
              >
                <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-1 border-b border-slate-800 pb-2">
                  <span className="text-indigo-400 font-bold">
                    Block #{events.length - idx} • Event: {evt.event_id}
                  </span>
                  <span className="text-slate-500 text-[11px]">{evt.timestamp}</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[11px] text-slate-400">
                  <div>
                    <span className="text-slate-500 block">Previous Block Hash:</span>
                    <span className="text-slate-400 break-all select-all">{evt.prev_hash}</span>
                  </div>
                  <div>
                    <span className="text-emerald-500 block font-bold">Current SHA-256 Hash:</span>
                    <span className="text-emerald-400 break-all select-all font-bold">{evt.event_hash}</span>
                  </div>
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 text-[11px] text-slate-300">
                  <span className="text-slate-500 block mb-1">Canonical Audit Finding Snapshot:</span>
                  <pre className="overflow-x-auto text-slate-300 font-mono">
                    {JSON.stringify(evt.payload, null, 2)}
                  </pre>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
