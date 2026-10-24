import type { Verdict } from "@/lib/types";

export function VerdictBadge({ verdict }: { verdict: Verdict }) {
  return <span data-verdict={verdict}>{verdict}</span>;
}
