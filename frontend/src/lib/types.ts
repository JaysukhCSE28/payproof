export type Verdict = "MATCH" | "DISCREPANCY" | "CANNOT_DETERMINE";

export interface Trip {
  trip_id: string;
}

export interface Finding {
  finding_id: string;
  trip_id: string;
  verdict: Verdict;
}

export interface LedgerEvent {
  event_id: string;
  finding_id: string;
  prev_hash: string;
  event_hash: string;
}
