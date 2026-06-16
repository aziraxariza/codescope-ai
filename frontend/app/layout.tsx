import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CodeScope AI",
  description: "GraphRAG-powered autonomous code intelligence platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
