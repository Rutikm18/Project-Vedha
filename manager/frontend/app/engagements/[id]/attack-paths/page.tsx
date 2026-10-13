"use client";

import { use } from "react";
import { AttackPathsWorkspace } from "./AttackPathsWorkspace";
import { AttackChainWorkspace } from "../../../../components/attack-paths/AttackChainWorkspace";

export default function AttackPathsPage({ params, searchParams }: { params: Promise<{ id: string }>; searchParams: Promise<{ mode?: string | string[]; finding?: string | string[] }> }) {
  const { id } = use(params);
  const query = use(searchParams);
  if (process.env.NEXT_PUBLIC_ATTACK_ASSESSMENTS_ENABLED === "true" && query.mode !== "network") return <AttackChainWorkspace engagementId={id} findingId={typeof query.finding === "string" ? query.finding : undefined} />;
  return <AttackPathsWorkspace engagementId={id} />;
}
