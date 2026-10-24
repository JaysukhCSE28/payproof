"use client";

import React, { useState } from "react";
import { approveFinding, rejectFinding } from "../lib/api";

interface Props {
  findingId: string;
  isApproved: boolean;
  onStatusChange: (status: "approved" | "rejected") => void;
}

export const ApprovalBar: React.FC<Props> = ({ findingId, isApproved, onStatusChange }) => {
  const [loading, setLoading] = useState(false);

  const handleApprove = async () => {
    setLoading(true);
    try {
      const res = await approveFinding(findingId);
      alert(res.message);
      onStatusChange("approved");
    } catch (err: any) {
      alert(`Approval error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    try {
      const res = await rejectFinding(findingId, "Waived by worker during review");
      alert(res.message);
      onStatusChange("rejected");
    } catch (err: any) {
      alert(`Rejection error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (isApproved) {
    return (
      <div className="bg-emerald-950/40 border border-emerald-500/30 p-4 rounded-xl flex items-center justify-between">
        <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
          <span>✓</span>
          <span>Explicitly Approved & Recorded to Tamper-Evident Ledger</span>
        </div>
        <span className="text-xs text-slate-400">Canonical SHA-256 Block Written</span>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <p className="text-sm font-semibold text-slate-200">Human-in-the-Loop Review Gate</p>
        <p className="text-xs text-slate-400 mt-0.5">
          Explicit approval required to commit finding to the audit ledger. PayProof never auto-files grievances.
        </p>
      </div>

      <div className="flex gap-3 w-full sm:w-auto">
        <button
          onClick={handleReject}
          disabled={loading}
          className="flex-1 sm:flex-none px-4 py-2 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
        >
          Waive / Reject
        </button>
        <button
          onClick={handleApprove}
          disabled={loading}
          className="flex-1 sm:flex-none px-5 py-2 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white transition shadow-lg shadow-emerald-950/50"
        >
          {loading ? "Committing..." : "Approve & Write to Ledger"}
        </button>
      </div>
    </div>
  );
};
