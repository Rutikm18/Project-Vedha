"use client";

import { use } from "react";
import { AttackPathsWorkspace } from "./AttackPathsWorkspace";

export default function AttackPathsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  return <AttackPathsWorkspace engagementId={id} />;
}
