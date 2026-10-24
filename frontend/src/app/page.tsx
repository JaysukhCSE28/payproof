import { UploadPanel } from "@/components/UploadPanel";

export default function HomePage() {
  return (
    <main>
      <h1>PayProof</h1>
      <p>Upload trips and review the audit matrix.</p>
      <UploadPanel />
      {/* TODO: trip matrix table */}
    </main>
  );
}
