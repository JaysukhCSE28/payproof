export function ApprovalBar({ findingId }: { findingId: string }) {
  return (
    <section>
      <h2>Review</h2>
      {/* TODO: POST /review/{findingId}/approve and /reject */}
      <p>Finding {findingId}</p>
    </section>
  );
}
