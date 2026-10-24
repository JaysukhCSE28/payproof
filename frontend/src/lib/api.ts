import { Trip, Finding, LedgerEvent, LedgerVerificationResult } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadTripsCsv(file: File): Promise<{ status: string; trips_ingested: number; sample_trip_ids: string[] }> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/ingest/trips`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function listTrips(): Promise<Trip[]> {
  const res = await fetch(`${API_BASE}/ingest/trips`);
  if (!res.ok) throw new Error("Failed to fetch trips");
  return res.json();
}

export async function runBatchAudit(): Promise<Finding[]> {
  const res = await fetch(`${API_BASE}/audit/batch`, { method: "POST" });
  if (!res.ok) throw new Error("Batch audit failed");
  return res.json();
}

export async function runTripAudit(tripId: string): Promise<Finding> {
  const res = await fetch(`${API_BASE}/audit/${tripId}`, { method: "POST" });
  if (!res.ok) throw new Error(`Audit for trip ${tripId} failed`);
  return res.json();
}

export async function listFindings(): Promise<Finding[]> {
  const res = await fetch(`${API_BASE}/audit/findings`);
  if (!res.ok) throw new Error("Failed to fetch findings");
  return res.json();
}

export async function getFinding(findingId: string): Promise<Finding> {
  const res = await fetch(`${API_BASE}/audit/finding/${findingId}`);
  if (!res.ok) throw new Error("Failed to fetch finding");
  return res.json();
}

export async function listQuarantined(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/audit/quarantine/list`);
  if (!res.ok) throw new Error("Failed to fetch quarantine list");
  return res.json();
}

export async function approveFinding(findingId: string): Promise<{ status: string; message: string; ledger_event: LedgerEvent }> {
  const res = await fetch(`${API_BASE}/review/${findingId}/approve`, { method: "POST" });
  if (!res.ok) throw new Error("Approval failed");
  return res.json();
}

export async function rejectFinding(findingId: string, reason?: string): Promise<{ status: string; message: string }> {
  const res = await fetch(`${API_BASE}/review/${findingId}/reject?reason=${encodeURIComponent(reason || "")}`, { method: "POST" });
  if (!res.ok) throw new Error("Rejection failed");
  return res.json();
}

export async function listLedger(): Promise<LedgerEvent[]> {
  const res = await fetch(`${API_BASE}/ledger`);
  if (!res.ok) throw new Error("Failed to fetch ledger");
  return res.json();
}

export async function verifyLedger(): Promise<LedgerVerificationResult> {
  const res = await fetch(`${API_BASE}/ledger/verify`);
  if (!res.ok) throw new Error("Ledger verification request failed");
  return res.json();
}
