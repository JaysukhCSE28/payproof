export type Verdict = "MATCH" | "DISCREPANCY" | "CANNOT_DETERMINE";
export type ReviewStatus = "pending" | "approved" | "rejected";

export interface Trip {
  trip_id: string;
  employee_id?: string;
  occurred_at?: string;
  zone?: string;
  city?: string;
  vendor?: string;
  vehicle_type?: string;
  trip_type?: string;
  distance_km?: string;
  claimed_fare_inr?: string;
  claimed_toll_inr?: string;
  claimed_parking_inr?: string;
  claimed_wait_inr?: string;
  wait_minutes?: string;
  is_night?: boolean;
  ocr_confidence?: number;
  ocr_text?: string;
  notes?: string;
  planted_error?: string;
}

export interface RuleCardFormula {
  base_fare_inr: string;
  per_km_inr: string;
  night_multiplier: string;
  airport_surcharge_inr: string;
  wait_per_min_inr: string;
  max_toll_inr: string;
  max_parking_inr: string;
  vehicle_multipliers: Record<string, string>;
}

export interface RuleCard {
  rule_id: string;
  version: number;
  status: "reviewed";
  clause_id: string;
  zone?: string;
  trip_type?: string;
  effective_from: string;
  effective_to?: string | null;
  formula: RuleCardFormula;
}

export interface Finding {
  finding_id: string;
  trip_id: string;
  verdict: Verdict;
  claimed_fare_inr?: string | null;
  computed_fare_inr?: string | null;
  verified_fare_inr?: string | null;
  engine_delta_inr?: string | null;
  tolerance_inr: string;
  rule_id?: string | null;
  clause_id?: string | null;
  evidence_packet_id?: string | null;
  review_status: ReviewStatus;
  reason?: string | null;
  breakdown?: Record<string, any> | null;
  execution_log?: string[] | null;
}

export interface LedgerEvent {
  event_id: string;
  finding_id?: string;
  payload: Record<string, any>;
  prev_hash: string;
  event_hash: string;
  timestamp: string;
}

export interface LedgerVerificationResult {
  valid: boolean;
  total_blocks: number;
  broken_at_event_id?: string;
  block_number?: number;
  reason?: string;
  message?: string;
}
