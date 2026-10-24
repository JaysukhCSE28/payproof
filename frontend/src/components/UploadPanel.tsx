"use client";

import React, { useState } from "react";
import { uploadTripsCsv } from "../lib/api";

interface Props {
  onUploadSuccess: () => void;
}

export const UploadPanel: React.FC<Props> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [msg, setMsg] = useState("");

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setMsg("");
    try {
      const res = await uploadTripsCsv(file);
      setMsg(`Successfully ingested ${res.trips_ingested} trips from ${file.name}!`);
      onUploadSuccess();
    } catch (err: any) {
      setMsg(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-white">Ingest Trip Evidence</h2>
          <p className="text-xs text-slate-400 mt-1">
            Upload CSV exports or receipts. Unreliable OCR inputs (&lt;80% conf) are automatically quarantined.
          </p>
        </div>
        <span className="text-[11px] font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
          Synthetic Demo Ready
        </span>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <label className="flex-1 cursor-pointer border-2 border-dashed border-slate-700 hover:border-emerald-500/50 bg-slate-950 p-6 rounded-xl flex flex-col items-center justify-center text-center transition">
          <span className="text-sm font-semibold text-slate-200">
            {uploading ? "Parsing & Validating..." : "Select CSV Trip Batch"}
          </span>
          <span className="text-xs text-slate-500 mt-1">Accepts CSV with trip_id, distance, claimed fare</span>
          <input
            type="file"
            accept=".csv"
            disabled={uploading}
            onChange={handleFile}
            className="hidden"
          />
        </label>
      </div>

      {msg && (
        <p className={`text-xs font-mono p-2 rounded ${msg.includes("failed") ? "bg-rose-950/40 text-rose-300" : "bg-emerald-950/40 text-emerald-300"}`}>
          {msg}
        </p>
      )}
    </div>
  );
};
