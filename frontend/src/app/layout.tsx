import type { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "PayProof",
  description: "Local-first trip-claim auditor",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
