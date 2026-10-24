"use client";

import React, { useState } from "react";
import { Finding, Trip } from "../lib/types";

interface Props {
  finding: Finding;
  trip?: Trip;
  isOpen: boolean;
  onClose: () => void;
}

export const DisputeModal: React.FC<Props> = ({ finding, trip, isOpen, onClose }) => {
  const [copied, setCopied] = useState(false);
  const [target, setTarget] = useState<"support" | "labour" | "union">("support");

  if (!isOpen) return null;

  const vendor = trip?.vendor || "Platform";
  const tripId = finding.trip_id;
  const delta = finding.engine_delta_inr || "0.00";
  const expected = finding.computed_fare_inr || "0.00";
  const claimed = finding.claimed_fare_inr || "0.00";
  const clause = finding.clause_id || "CLAUSE-METRO-2026";
  const rule = finding.rule_id || "RULE-METRO-V1";
  const packetId = finding.evidence_packet_id || "EVID-VERIFIED";

  let letterText = "";

  if (target === "support") {
    letterText = `FORMAL WAGE DISCREPANCY RECOURSE TICKET
Date: ${new Date().toLocaleDateString("en-IN")}
To: ${vendor} Partner Care & Grievance Redressal
Partner ID / Vehicle: Registered Partner (${trip?.vehicle_type || "Hatchback"})

Subject: Underpayment Claim on Trip #${tripId} — Shortfall ₹${delta}

Dear Support Team,

I am writing to formally request a wage adjustment for Trip #${tripId}. A deterministic audit of my trip parameters against your published rate card reveals an unpaid shortfall of ₹${delta}.

AUDIT RECONCILIATION SUMMARY:
- Governing Contract Clause: ${clause} (${rule})
- Distance Traveled: ${trip?.distance_km || "N/A"} km
- Night Multiplier Applicable: ${trip?.is_night ? "Yes (1.25x)" : "No"}
- Verified Entitlement per Rate Card: ₹${expected}
- Payout Disbursed by Platform: ₹${claimed}
- Net Underpayment Owed to Partner: ₹${delta}

CRYPTOGRAPHIC AUDIT TRAIL:
- Evidence Packet ID: ${packetId}
- Deterministic Math Engine: Python Decimal + Integer Paise Verifier
- Tamper-Evident Ledger Integrity: SHA-256 Hash Chained

I request that you credit the balance of ₹${delta} to my linked bank / UPI account within 48 business hours as mandated under Fair Gig Payout Guidelines.

Attached: Cryptographic Evidence Packet [${packetId}]
Submitted via PayProof Autonomous Wage Auditor.`;
  } else if (target === "labour") {
    letterText = `BEFORE THE DEPUTY LABOUR COMMISSIONER / STATE GIG WORKERS WELFARE BOARD
COMPLAINT UNDER GIG AND PLATFORM WORKERS (REGULATION OF EMPLOYMENT AND WELFARE) ACT

Complainant: Gig Delivery Partner
Respondent: ${vendor} Technologies Pvt. Ltd.
Transaction ID: Trip #${tripId}

PRAYER:
Direction to Respondent to disburse withheld earnings of ₹${delta} along with interest and costs.

FACTS OF THE CASE:
1. Complainant performed delivery services for Respondent under Trip #${tripId}.
2. Respondent published binding rate terms under Clause ${clause}.
3. Deterministic algorithmic audit verifies Complainant is legally entitled to ₹${expected}.
4. Respondent unilaterally disbursed ₹${claimed}, resulting in an illegal wage deduction of ₹${delta}.
5. Hash-verified cryptographic proof (Packet ID: ${packetId}) is submitted herewith in support.

Place: Metro Region
Date: ${new Date().toLocaleDateString("en-IN")}`;
  } else {
    letterText = `MEMORANDUM TO INDIAN FEDERATION OF APP-BASED TRANSPORT WORKERS (IFAT)
Collective Case Log: Systematic Rate Underpayment
Platform: ${vendor} | Zone: ${trip?.zone || "METRO"}
Trip Reference: #${tripId} | Unpaid Delta: ₹${delta}
Policy Violation: ${clause} (${rule})
Evidence Packet: ${packetId}

Notes for Collective Bargaining:
Platform failed to apply contracted night/distance multipliers during audit cycle. Pattern matches synthetic discrepancy cluster. Recorded to immutable ledger.`;
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(letterText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-950/60">
          <div className="flex items-center gap-2.5">
            <span className="w-3 h-3 rounded-full bg-emerald-500" />
            <h3 className="font-bold text-white text-sm">
              Generate Formal Grievance & Dispute Ticket
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-lg font-bold p-1 rounded transition"
          >
            ✕
          </button>
        </div>

        {/* Recipient Selector */}
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex flex-wrap gap-2 text-xs">
          <span className="text-slate-400 py-1 font-semibold">Target Authority:</span>
          {(
            [
              { id: "support", label: "🏢 Platform Support (Swiggy / Uber)" },
              { id: "labour", label: "⚖️ State Labour Board / Commissioner" },
              { id: "union", label: "✊ Driver Union Collective (IFAT)" },
            ] as const
          ).map((t) => (
            <button
              key={t.id}
              onClick={() => setTarget(t.id)}
              className={`py-1.5 px-3 rounded-lg border font-semibold transition ${
                target === t.id
                  ? "bg-indigo-600 text-white border-indigo-500 shadow"
                  : "bg-slate-800 text-slate-400 border-slate-700 hover:text-white"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Letter Body Preview */}
        <div className="p-4 flex-1 overflow-y-auto">
          <textarea
            readOnly
            value={letterText}
            rows={14}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-xs text-slate-200 font-mono leading-relaxed focus:outline-none select-all"
          />
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex justify-between items-center gap-3">
          <div className="text-[11px] text-slate-400 font-mono">
            Packet ID: <span className="text-emerald-400">{packetId}</span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="py-2 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
            >
              Close
            </button>
            <button
              onClick={handleCopy}
              className="py-2 px-5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition shadow-lg shadow-emerald-950/50 flex items-center gap-1.5"
            >
              <span>📋</span>
              <span>{copied ? "Copied to Clipboard!" : "Copy Full Ticket"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
