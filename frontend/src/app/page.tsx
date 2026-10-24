"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { UploadPanel } from "../components/UploadPanel";
import { VerdictBadge } from "../components/VerdictBadge";
import { listTrips, listFindings, runBatchAudit } from "../lib/api";
import { Trip, Finding } from "../lib/types";

export default function HomePage() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(false);
  const [auditing, setAuditing] = useState(false);
  const [filter, setFilter] = useState<string>("ALL");

  const loadData = async () => {
    setLoading(true);
    try {
      const [tList, fList] = await Promise.all([listTrips(), listFindings()]);
      setTrips(tList);
      setFindings(fList);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunBatchAudit = async () => {
    setAuditing(true);
    try {
      const results = await runBatchAudit();
      setFindings(results);
    } catch (err: any) {
      alert(`Batch audit error: ${err.message}`);
    } finally {
      setAuditing(false);
    }
  };

  const findingMap = new Map(findings.map((f) => [f.trip_id, f]));

  const filteredTrips = trips.filter((t) => {
    const f = findingMap.get(t.trip_id);
    if (filter === "ALL") return true;
    if (filter === "UNAUDITED") return !f;
    return f?.verdict === filter;
  });

  const discrepancyCount = findings.filter((f) => f.verdict === "DISCREPANCY").length;
  const matchCount = findings.filter((f) => f.verdict === "MATCH").length;
  const cannotCount = findings.filter((f) => f.verdict === "CANNOT_DETERMINE").length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Top Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50 px-6 py-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block animate-pulse" />
              PayProof
            </span>
            <span className="bg-amber-500/10 text-amber-400 text-xs px-2.5 py-0.5 rounded-full border border-amber-500/20 font-mono">
              Synthetic Demo Fixtures
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic AI-Math Decoupling • Autonomous Wage Transparency for Gig Workers
          </p>
        </div>

        <nav className="flex items-center gap-3 text-xs font-medium">
          <Link href="/" className="px-3 py-1.5 rounded-lg bg-slate-800 text-white border border-slate-700">
            Trips Matrix
          </Link>
          <Link href="/ledger" className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            Audit Ledger
          </Link>
          <Link href="/quarantine" className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            Quarantine ({cannotCount})
          </Link>
          <Link href="/results" className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            Benchmark Results
          </Link>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Upload & Audit Trigger */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <UploadPanel onUploadSuccess={loadData} />
          </div>

          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl flex flex-col justify-between space-y-4">
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Audit Engine Core</h2>
              <p className="text-xs text-slate-400 mt-1">
                Executes Decimal math and integer-paise verification across all ingested trips in parallel.
              </p>
            </div>

            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between text-slate-400">
                <span>Ingested Trips:</span>
                <span className="text-white font-bold">{trips.length}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Discrepancies (&gt;₹1):</span>
                <span className="text-rose-400 font-bold">{discrepancyCount}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Matches (≤₹1):</span>
                <span className="text-emerald-400 font-bold">{matchCount}</span>
              </div>
            </div>

            <button
              onClick={handleRunBatchAudit}
              disabled={auditing || trips.length === 0}
              className="w-full py-3 px-4 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white text-xs font-bold transition shadow-lg shadow-indigo-950/50"
            >
              {auditing ? "Executing Deterministic Sandbox..." : "Run Batch Deterministic Audit"}
            </button>
          </div>
        </div>

        {/* Matrix Filter & Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Trip Audit Matrix ({filteredTrips.length})
              </h3>
              <p className="text-xs text-slate-400">Click any row to inspect calculations, citations, and execution logs.</p>
            </div>

            <div className="flex gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-mono">
              {["ALL", "DISCREPANCY", "MATCH", "CANNOT_DETERMINE", "UNAUDITED"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setFilter(tab)}
                  className={`px-3 py-1 rounded transition ${
                    filter === tab ? "bg-slate-800 text-white font-bold" : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950/80 text-slate-400 uppercase text-[11px] font-mono tracking-wider border-b border-slate-800">
                <tr>
                  <th className="p-3.5">Trip ID</th>
                  <th className="p-3.5">Platform</th>
                  <th className="p-3.5">Distance</th>
                  <th className="p-3.5">Claimed Paid</th>
                  <th className="p-3.5">Computed Expected</th>
                  <th className="p-3.5">Delta</th>
                  <th className="p-3.5">Verdict</th>
                  <th className="p-3.5">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[12px]">
                {filteredTrips.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="p-8 text-center text-slate-500 italic">
                      No trips match the selected filter.
                    </td>
                  </tr>
                ) : (
                  filteredTrips.map((t) => {
                    const finding = findingMap.get(t.trip_id);
                    return (
                      <tr key={t.trip_id} className="hover:bg-slate-800/40 transition">
                        <td className="p-3.5 font-bold text-white">{t.trip_id}</td>
                        <td className="p-3.5 text-slate-300 font-sans">{t.vendor || "Swiggy"} ({t.zone || "METRO"})</td>
                        <td className="p-3.5">{t.distance_km} km</td>
                        <td className="p-3.5">₹{t.claimed_fare_inr}</td>
                        <td className="p-3.5 text-emerald-400 font-bold">
                          {finding?.computed_fare_inr ? `₹${finding.computed_fare_inr}` : "—"}
                        </td>
                        <td className="p-3.5 font-bold">
                          {finding?.engine_delta_inr ? (
                            <span className={parseFloat(finding.engine_delta_inr) > 1 ? "text-rose-400" : "text-emerald-400"}>
                              ₹{parseFloat(finding.engine_delta_inr) > 0 ? "+" : ""}{finding.engine_delta_inr}
                            </span>
                          ) : (
                            "—"
                          )}
                        </td>
                        <td className="p-3.5">
                          {finding ? (
                            <VerdictBadge verdict={finding.verdict} />
                          ) : (
                            <span className="text-slate-500 text-xs">Pending Audit</span>
                          )}
                        </td>
                        <td className="p-3.5">
                          <Link
                            href={`/audit/${t.trip_id}`}
                            className="inline-block px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs transition border border-slate-700"
                          >
                            Inspect →
                          </Link>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
