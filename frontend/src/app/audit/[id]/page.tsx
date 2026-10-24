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
import { DisputeModal } from "../../../components/DisputeModal";

export default function AuditDetailPage() {
  const params = useParams();
  const tripId = params?.id as string;

  const [finding, setFinding] = useState<Finding | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showDisputeModal, setShowDisputeModal] = useState(false);
  const [briefingLang, setBriefingLang] = useState<"en" | "hi" | "ta">("hi");

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

  const delta = finding?.engine_delta_inr || "0.00";
  const expected = finding?.computed_fare_inr || "0.00";
  const claimed = finding?.claimed_fare_inr || "0.00";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Navigation & Header */}
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <Link
            href="/"
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition font-mono"
          >
            ← Back to Audit Workspace
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
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                <div>
                  <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-3">
                    <span>Trip {finding.trip_id}</span>
                    <span className="text-xs font-sans font-normal px-2.5 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-slate-300">
                      Packet ID: {finding.evidence_packet_id || "EVID-VERIFIED"}
                    </span>
                  </h1>
                  <p className="text-xs text-slate-400 mt-1">{finding.reason}</p>
                </div>

                {finding.verdict === "DISCREPANCY" && (
                  <button
                    onClick={() => setShowDisputeModal(true)}
                    className="py-2 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition shadow-lg shadow-emerald-950/50 flex items-center gap-2 self-start sm:self-auto"
                  >
                    <span>📋</span>
                    <span>1-Click Dispute Ticket</span>
                  </button>
                )}
              </div>

              {/* Multi-Lingual Driver Briefing Card */}
              {finding.verdict === "DISCREPANCY" && (
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      Driver Regional Briefing (15M Worker View):
                    </span>
                    <div className="flex gap-1 text-[11px] font-semibold">
                      {(["hi", "en", "ta"] as const).map((l) => (
                        <button
                          key={l}
                          onClick={() => setBriefingLang(l)}
                          className={`px-2 py-0.5 rounded ${
                            briefingLang === l ? "bg-slate-800 text-white font-bold" : "text-slate-500 hover:text-slate-300"
                          }`}
                        >
                          {l === "hi" ? "हिन्दी" : l === "ta" ? "தமிழ்" : "English"}
                        </button>
                      ))}
                    </div>
                  </div>

                  <p className="text-xs text-slate-200 leading-relaxed font-sans">
                    {briefingLang === "hi" && (
                      <>
                        इस ट्रिप में <strong>₹{delta}</strong> का कम भुगतान मिला है। कंपनी ने ₹{claimed} दिया, जबकि रेट कार्ड के अनुसार <strong>₹{expected}</strong> बनता था। नाइट मल्टीप्लायर (1.25x) या वेटिंग टाइम नहीं जोड़ा गया था।
                      </>
                    )}
                    {briefingLang === "en" && (
                      <>
                        Underpayment of <strong>₹{delta}</strong> detected. Platform paid ₹{claimed}, whereas governing rate card warrants <strong>₹{expected}</strong>. Night multiplier or waiting allowance was omitted.
                      </>
                    )}
                    {briefingLang === "ta" && (
                      <>
                        இந்த பயணத்தில் <strong>₹{delta}</strong> குறைவாக வழங்கப்பட்டுள்ளது. நிறுவனம் ₹{claimed} செலுத்தியது, ஆனால் ஒப்பந்தத்தின்படி <strong>₹{expected}</strong> வர வேண்டும். இரவு கூடுதல் கட்டணம் சேர்க்கப்படவில்லை.
                      </>
                    )}
                  </p>
                </div>
              )}
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

            {/* Dispute Modal */}
            <DisputeModal
              finding={finding}
              isOpen={showDisputeModal}
              onClose={() => setShowDisputeModal(false)}
            />
          </>
        ) : null}
      </div>
    </div>
  );
}
