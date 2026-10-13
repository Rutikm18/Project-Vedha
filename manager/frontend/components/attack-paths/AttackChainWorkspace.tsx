"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { PageShell } from "../PageShell";
import { AttackAssessmentsPanel } from "./AttackAssessmentsPanel";
import { AttackPathModeNav } from "./AttackPathModeNav";
import { fetchJson } from "../../lib/fetcher";

export function AttackChainWorkspace({ engagementId, findingId }: { engagementId: string; findingId?: string }) {
  const engagement = useQuery({ queryKey: ["engagement-name", engagementId], queryFn: () => fetchJson<{ name?: string }>(`/api/engagements/${encodeURIComponent(engagementId)}`), retry: false });
  return <PageShell title="Attack paths" subtitle={engagement.data?.name ?? "Finding-driven investigation"} headerActions={<Link className="assessment-link" href={`/engagements/${encodeURIComponent(engagementId)}`}>Back to engagement</Link>} hideRefresh>
    <AttackPathModeNav engagementId={engagementId} mode="chains" />
    <AttackAssessmentsPanel key={`${engagementId}:${findingId ?? ""}`} engagementId={engagementId} initialFindingId={findingId} />
  </PageShell>;
}
