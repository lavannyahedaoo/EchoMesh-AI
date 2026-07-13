import type { Metadata } from "next";
import "./globals.css";
import QueryProvider from "../context/QueryProvider";
import { WorkspaceProvider } from "../context/WorkspaceContext";

export const metadata: Metadata = {
  title: "EchoMesh AI — Memory OS",
  description: "AI-native knowledge graph database, decisions tracker, and semantic memory operating system for software teams.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased bg-slate-950 text-slate-100 min-h-screen">
        <QueryProvider>
          <WorkspaceProvider>
            {children}
          </WorkspaceProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
