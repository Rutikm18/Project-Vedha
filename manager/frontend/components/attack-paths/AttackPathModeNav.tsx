import Link from "next/link";
import { GitBranch, Network } from "lucide-react";
import "./attack-assessments.css";

export function AttackPathModeNav({ engagementId, mode }: { engagementId: string; mode: "chains" | "network" }) {
  const url = `/engagements/${encodeURIComponent(engagementId)}/attack-paths`;
  return <nav className="attack-path-modes" aria-label="Attack-path view">
    <Link href={url} aria-current={mode === "chains" ? "page" : undefined}><GitBranch size={15} aria-hidden="true" />Finding chains</Link>
    <Link href={`${url}?mode=network`} aria-current={mode === "network" ? "page" : undefined}><Network size={15} aria-hidden="true" />Network overview</Link>
  </nav>;
}
