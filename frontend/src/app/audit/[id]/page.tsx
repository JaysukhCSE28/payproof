"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { runTripAudit } from "../../../lib/api";
import { Finding } from "../../../lib/types";
import { AmountCards } from "../../../components/AmountCards";
import { CalcBreakdown } from "../../../components/CalcBreakdown";
import { ClauseViewer } from "../../../components/ClauseViewer";
import { ExecutionLog } from "../../../components/ExecutionLog";
import { ApprovalBar } from "../../../components/ApprovalBar";
import { VerdictBadge } from "../../../components/VerdictBadge";

export default function AuditDetailPage() {
  const params = useParams();
  const tripId = params?.id as string;

  const [finding, setFinding] = useState<Finding | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadAudit = async () => {
    if (!tripId) return;
    setLoading(true);
    setError("");
    try {
      const res = await runTripAudit(tripId);
      setFinding(res);
    } catch (err: any) {
      setError(err.message || "Failed to audit trip");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAudit();
  }, [tripId]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Navigation & Header */}
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <Link
            href="/"
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition font-mono"
          >
            ← Back to Matrix
          </Link>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-slate-400">Trip Audit Inspector</span>
            {finding && <VerdictBadge verdict={finding.verdict} />}
          </div>
        </div>

        {loading ? (
          <div className="bg-slate-900 border border-slate-800 p-12 rounded-xl text-center text-slate-400 font-mono text-sm">
            Executing deterministic audit sandbox for {tripId}...
          </div>
        ) : error ? (
          <div className="bg-rose-950/40 border border-rose-500/40 p-6 rounded-xl text-rose-300 space-y-2">
            <h3 className="font-bold text-base">Audit Failed</h3>
            <p className="text-sm font-mono">{error}</p>
          </div>
        ) : finding ? (
          <>
            {/* Finding Overview */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-2">
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                <h1 className="text-2xl font-bold font-mono text-white tracking-tight">
                  Trip {finding.trip_id}
                </h1>
                <span className="text-xs font-mono text-slate-500">
                  Finding ID: {finding.finding_id}
                </span>
              </div>
              <p className="text-xs text-slate-400">{finding.reason}</p>
            </div>

            {/* Amount Cards */}
            <AmountCards
              claimedFare={finding.claimed_fare_inr || "0.00"}
              computedFare={finding.computed_fare_inr}
              difference={finding.engine_delta_inr}
              tolerance={finding.tolerance_inr}
            />

            {/* Side-by-side details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <CalcBreakdown breakdown={finding.breakdown} />
              <ClauseViewer
                clauseId={finding.clause_id}
                ruleId={finding.rule_id}
                citation={finding.breakdown?.citation}
              />
            </div>

            {/* Execution Trace */}
            <ExecutionLog log={finding.execution_log} />

            {/* Approval Gate */}
            {finding.verdict === "DISCREPANCY" && (
              <ApprovalBar
                findingId={finding.finding_id}
                isApproved={finding.review_status === "approved"}
                onStatusChange={(newStatus) => {
                  setFinding((prev) => (prev ? { ...prev, review_status: newStatus } : null));
                }}
              />
            )}
          </>
        ) : null}
      </div>
    </div>
  );
}
