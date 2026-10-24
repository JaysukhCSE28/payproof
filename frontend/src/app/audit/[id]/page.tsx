import { AmountCards } from "@/components/AmountCards";
import { ApprovalBar } from "@/components/ApprovalBar";
import { CalcBreakdown } from "@/components/CalcBreakdown";
import { ClauseViewer } from "@/components/ClauseViewer";
import { ExecutionLog } from "@/components/ExecutionLog";
import { VerdictBadge } from "@/components/VerdictBadge";

export default function AuditDetailPage({ params }: { params: { id: string } }) {
  return (
    <main>
      <h1>Inspection {params.id}</h1>
      <VerdictBadge verdict="CANNOT_DETERMINE" />
      <AmountCards />
      <CalcBreakdown />
      <ClauseViewer />
      <ApprovalBar findingId={params.id} />
      <ExecutionLog />
    </main>
  );
}
