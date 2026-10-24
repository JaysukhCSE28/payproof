"use client";

import React, { useState } from "react";
import { Finding, Trip } from "../lib/types";

interface Props {
  trips: Trip[];
  findings: Finding[];
}

type Language = "en" | "hi" | "ta" | "te";

export const DriverMobileView: React.FC<Props> = ({ trips, findings }) => {
  const [selectedTripId, setSelectedTripId] = useState<string>(
    findings.find((f) => f.verdict === "DISCREPANCY")?.trip_id || trips[0]?.trip_id || ""
  );
  const [lang, setLang] = useState<Language>("hi");
  const [copied, setCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const findingMap = new Map(findings.map((f) => [f.trip_id, f]));
  const currentTrip = trips.find((t) => t.trip_id === selectedTripId);
  const currentFinding = findingMap.get(selectedTripId);

  const delta = currentFinding?.engine_delta_inr || "0.00";
  const claimed = currentFinding?.claimed_fare_inr || currentTrip?.claimed_fare_inr || "0.00";
  const expected = currentFinding?.computed_fare_inr || "0.00";
  const vendor = currentTrip?.vendor || "Platform";
  const clause = currentFinding?.clause_id || "CLAUSE-METRO-2026";

  // Multi-lingual translations
  const messages = {
    en: {
      greeting: "Hello Partner! 🙏",
      intro: `Your audit for Trip #${selectedTripId} on ${vendor} is complete.`,
      claimedLabel: "Platform Paid You",
      expectedLabel: "Governing Rate Card Owed",
      deltaUnder: `Underpayment Detected: You were shortchanged by ₹${delta}.`,
      deltaMatch: "Payout Verified: Fare matches approved rate card.",
      clauseLabel: "Governing Policy",
      ledgerLabel: "Cryptographic Audit Proof",
      audioLabel: "Voice Summary in English",
      copyBtn: "Copy WhatsApp Dispute to Support",
      unionBtn: "Export Proof to Driver Union",
      copiedToast: "Copied! Paste into Swiggy / Uber Support chat.",
    },
    hi: {
      greeting: "नमस्ते साथी! 🙏",
      intro: `${vendor} की ट्रिप #${selectedTripId} का ऑडिट पूरा हो गया है।`,
      claimedLabel: "कंपनी ने दिया",
      expectedLabel: "रेट कार्ड के अनुसार बनता है",
      deltaUnder: `कम भुगतान मिला: आपको ₹${delta} कम दिए गए हैं!`,
      deltaMatch: "भुगतान सही है: रेट कार्ड के अनुसार पूरा भुगतान हुआ।",
      clauseLabel: "लागू पॉलिसी क्लॉज",
      ledgerLabel: "क्रिप्टोग्राफिक ऑडिट प्रूफ",
      audioLabel: "हिंदी में वॉयस समरी सुनें",
      copyBtn: "सपोर्ट के लिए शिकायत कॉपी करें (WhatsApp)",
      unionBtn: "ड्राइवर यूनियन को प्रूफ भेजें",
      copiedToast: "कॉपी हो गया! सीधे Swiggy / Uber सपोर्ट में पेस्ट करें।",
    },
    ta: {
      greeting: "வணக்கம் நண்பரே! 🙏",
      intro: `${vendor} இன் பயணம் #${selectedTripId} க்கான தணிக்கை முடிந்தது.`,
      claimedLabel: "நிறுவனம் செலுத்தியது",
      expectedLabel: "விதிமுறைகளின்படி வரவேண்டியது",
      deltaUnder: `குறைவான ஊதியம்: உங்களுக்கு ₹${delta} குறைவாக வழங்கப்பட்டுள்ளது!`,
      deltaMatch: "சரியான கட்டணம்: முழுத் தொகையும் பெறப்பட்டது.",
      clauseLabel: "கொள்கை விதிமுறை",
      ledgerLabel: "கிரிப்டோகிராஃபிக் ஆதாரம்",
      audioLabel: "தமிழில் குரல் சுருக்கத்தைக் கேளுங்கள்",
      copyBtn: "ஆதரவுக்கான புகாரை நகலெடுக்கவும்",
      unionBtn: "தொழிற்சங்கத்திற்கு ஆதாரத்தை அனுப்பவும்",
      copiedToast: "நகலெடுக்கப்பட்டது! ஆதரவு சாட்டில் ஒட்டவும்.",
    },
    te: {
      greeting: "నమస్కారం సోదరా! 🙏",
      intro: `${vendor} ట్రిప్ #${selectedTripId} ఆడిట్ పూర్తయింది.`,
      claimedLabel: "కంపెనీ చెల్లించినది",
      expectedLabel: "రూల్స్ ప్రకారం రావాల్సింది",
      deltaUnder: `తక్కువ చెల్లింపు: మీకు ₹${delta} తక్కువ చెల్లించబడింది!`,
      deltaMatch: "సరియైన చెల్లింపు: పూర్తి మొత్తం అందింది.",
      clauseLabel: "పాలసీ నిబంధన",
      ledgerLabel: "క్రిప్టోగ్రాఫిక్ ఆడిట్ రుజువు",
      audioLabel: "తెలుగులో వాయిస్ సారాంశం వినండి",
      copyBtn: "సపోర్ట్ కోసం ఫిర్యాదును కాపీ చేయండి",
      unionBtn: "యూనియన్‌కు రుజువును ఫార్వార్డ్ చేయండి",
      copiedToast: "కాపీ చేయబడింది! సపోర్ట్ చాట్‌లో పేస్ట్ చేయండి.",
    },
  };

  const t = messages[lang];

  const generateGrievanceText = () => {
    return `To: ${vendor} Partner Care Support
Regarding: Wage Discrepancy on Trip #${selectedTripId}
Calculated Entitlement: ₹${expected}
Amount Credited: ₹${claimed}
Discrepancy / Shortfall: ₹${delta}
Governing Policy Clause: ${clause}
Audit Status: Verified by PayProof Deterministic Engine
Evidence Packet ID: ${currentFinding?.evidence_packet_id || "EVID-VERIFIED"}
Ledger Verification: SHA-256 Canonical Chained Proof

Reason: Discrepancy identified in distance / multiplier calculation per reviewed rate card. 
Please review and credit the outstanding balance of ₹${delta} to my partner payout wallet immediately. Thank you.`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generateGrievanceText());
    setCopied(true);
    setTimeout(() => setCopied(false), 3000);
  };

  const handlePlayVoice = () => {
    setIsPlayingAudio(true);
    setTimeout(() => setIsPlayingAudio(false), 3500);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      {/* Left Column: Context & Controls */}
      <div className="lg:col-span-5 space-y-6">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
            Worker Quick-Audit Simulation
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            How 15M+ Gig Workers Use PayProof
          </h2>
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">
            Delivery partners don't use laptops or spreadsheets. They simply forward daily screenshot receipts
            to the <strong className="text-white">PayProof WhatsApp Bot</strong>. The bot analyzes the rate card, computes the exact paise delta, and replies in their native language with a ready-to-send dispute ticket.
          </p>

          <div className="mt-6 space-y-4 pt-4 border-t border-slate-800">
            {/* Language Selector */}
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-2">
                1. Select Worker Language:
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {(
                  [
                    { id: "hi", label: "🇮🇳 हिन्दी" },
                    { id: "en", label: "🇬🇧 English" },
                    { id: "ta", label: "🇮🇳 தமிழ்" },
                    { id: "te", label: "🇮🇳 తెలుగు" },
                  ] as const
                ).map((l) => (
                  <button
                    key={l.id}
                    onClick={() => setLang(l.id)}
                    className={`py-2 px-3 text-xs font-semibold rounded-lg border transition ${
                      lang === l.id
                        ? "bg-emerald-600 text-white border-emerald-500 shadow-md shadow-emerald-950/50"
                        : "bg-slate-800 text-slate-400 border-slate-700 hover:text-white"
                    }`}
                  >
                    {l.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Trip Selector */}
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-2">
                2. Select Audited Trip Receipt:
              </label>
              <select
                value={selectedTripId}
                onChange={(e) => setSelectedTripId(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
              >
                {trips.map((tr) => {
                  const f = findingMap.get(tr.trip_id);
                  const isDisc = f?.verdict === "DISCREPANCY";
                  return (
                    <option key={tr.trip_id} value={tr.trip_id}>
                      {tr.trip_id} — {tr.vendor} ({tr.zone}) {isDisc ? `[🚨 ₹${f?.engine_delta_inr} Underpaid]` : "[✓ MATCH]"}
                    </option>
                  );
                })}
              </select>
            </div>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl space-y-3 text-xs">
          <h4 className="font-bold text-slate-200 uppercase tracking-wider text-[11px]">
            Why This Solves Real-World Worker Friction
          </h4>
          <ul className="space-y-2 text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span><strong>Zero App Install:</strong> Works directly over WhatsApp or SMS without eating mobile storage.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span><strong>No Legal Intimidation:</strong> Converts complex contractual formulas into clear ₹ totals.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span><strong>Instant Recourse:</strong> Generates a pre-formatted grievance ready for 1-click platform support copy.</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Right Column: Sleek WhatsApp Mobile Simulator */}
      <div className="lg:col-span-7 flex justify-center">
        {/* Smartphone Shell */}
        <div className="w-full max-w-[380px] bg-slate-950 rounded-[44px] border-[6px] border-slate-800 shadow-2xl overflow-hidden shadow-emerald-950/20">
          {/* Phone Top Notch & Status Bar */}
          <div className="bg-[#0b141a] px-6 pt-3 pb-2 flex justify-between items-center text-[10px] text-slate-400 font-mono select-none">
            <span>9:41</span>
            <div className="w-20 h-4 bg-slate-900 rounded-full mx-auto" />
            <div className="flex items-center gap-1.5">
              <span>5G</span>
              <div className="w-4 h-2.5 border border-slate-400 rounded-sm p-0.5">
                <div className="w-full h-full bg-emerald-400 rounded-xs" />
              </div>
            </div>
          </div>

          {/* WhatsApp Header */}
          <div className="bg-[#1f2c34] px-4 py-3 flex items-center justify-between border-b border-[#2a3942]">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-full bg-emerald-700 flex items-center justify-center text-white font-bold text-sm shadow">
                PP
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="font-semibold text-xs text-white">PayProof Audit</span>
                  <span className="w-3.5 h-3.5 rounded-full bg-emerald-500 text-[9px] flex items-center justify-center text-black font-extrabold">✓</span>
                </div>
                <span className="text-[10px] text-emerald-400">Online • Automated Assistant</span>
              </div>
            </div>
            <div className="text-slate-400 text-xs font-mono">🔒 SHA-256</div>
          </div>

          {/* WhatsApp Chat Body */}
          <div className="bg-[#0b141a] p-4 min-h-[440px] flex flex-col justify-between space-y-3 font-sans text-xs">
            {/* Timestamp */}
            <div className="text-center">
              <span className="bg-[#182229] text-[10px] text-slate-400 px-3 py-1 rounded-lg">
                Today, 23:42
              </span>
            </div>

            {/* Inbound Message Bubble from Bot */}
            <div className="bg-[#202c33] text-slate-100 p-4 rounded-2xl rounded-tl-none border border-[#2a3942] space-y-3 shadow-md">
              <div className="flex justify-between items-start">
                <span className="font-bold text-emerald-400 text-sm">{t.greeting}</span>
                <span className="text-[10px] text-slate-400 font-mono">23:42</span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{t.intro}</p>

              {/* Financial Comparison Box */}
              <div className="bg-[#111b21] p-3 rounded-xl border border-[#222e35] space-y-2 font-mono">
                <div className="flex justify-between items-center text-slate-400 text-[11px]">
                  <span>{t.claimedLabel}:</span>
                  <span className="text-slate-200 font-bold">₹{claimed}</span>
                </div>
                <div className="flex justify-between items-center text-slate-400 text-[11px]">
                  <span>{t.expectedLabel}:</span>
                  <span className="text-emerald-400 font-bold">₹{expected}</span>
                </div>
                <div className="border-t border-[#222e35] pt-1.5 flex justify-between items-center text-xs">
                  <span className="font-sans font-bold text-slate-200">Difference:</span>
                  <span
                    className={`font-bold ${
                      currentFinding?.verdict === "DISCREPANCY" ? "text-rose-400" : "text-emerald-400"
                    }`}
                  >
                    {currentFinding?.verdict === "DISCREPANCY" ? `🚨 ₹${delta} Underpaid` : "✓ Exact Match"}
                  </span>
                </div>
              </div>

              {/* Status Message */}
              <div
                className={`p-2.5 rounded-lg text-xs leading-snug font-medium ${
                  currentFinding?.verdict === "DISCREPANCY"
                    ? "bg-rose-950/40 border border-rose-800/40 text-rose-300"
                    : "bg-emerald-950/40 border border-emerald-800/40 text-emerald-300"
                }`}
              >
                {currentFinding?.verdict === "DISCREPANCY" ? t.deltaUnder : t.deltaMatch}
              </div>

              {/* Clause & Proof Footnote */}
              <div className="text-[10px] text-slate-400 space-y-1 pt-1 border-t border-[#2a3942]">
                <div className="flex justify-between">
                  <span>{t.clauseLabel}:</span>
                  <span className="text-slate-300 font-mono">{clause}</span>
                </div>
                <div className="flex justify-between">
                  <span>Audit Engine:</span>
                  <span className="text-emerald-400 font-mono">Decimal + Paise (0 Hallucinations)</span>
                </div>
              </div>

              {/* Simulated Audio Voice Briefing */}
              <div className="bg-[#111b21] p-2.5 rounded-xl border border-[#222e35] flex items-center justify-between gap-3">
                <button
                  onClick={handlePlayVoice}
                  className="w-8 h-8 rounded-full bg-emerald-500 hover:bg-emerald-400 text-black flex items-center justify-center font-bold text-xs transition"
                >
                  {isPlayingAudio ? "⏸" : "▶"}
                </button>
                <div className="flex-1">
                  <div className="text-[11px] font-semibold text-slate-200">{t.audioLabel}</div>
                  <div className="h-1.5 bg-slate-800 rounded-full mt-1 overflow-hidden">
                    <div
                      className={`h-full bg-emerald-400 rounded-full transition-all duration-3000 ${
                        isPlayingAudio ? "w-full" : "w-1/3"
                      }`}
                    />
                  </div>
                </div>
                <span className="text-[10px] text-slate-400 font-mono">0:12</span>
              </div>
            </div>

            {/* Bottom 1-Click Action Buttons */}
            <div className="space-y-2 pt-2">
              <button
                onClick={handleCopy}
                className="w-full py-2.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-lg shadow-emerald-950/50 transition active:scale-95"
              >
                <span>📋</span>
                <span>{copied ? t.copiedToast : t.copyBtn}</span>
              </button>
              <button
                onClick={() => alert(`Evidence packet ${currentFinding?.evidence_packet_id} exported to Telangana Gig Workers Union portal.`)}
                className="w-full py-2 px-3 rounded-xl bg-[#1f2c34] hover:bg-[#2a3942] text-slate-300 font-semibold text-xs flex items-center justify-center gap-1.5 transition"
              >
                <span>⚖️</span>
                <span>{t.unionBtn}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
