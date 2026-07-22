"use client";

/**
 * Exposure analytics cards — Protocol Risk + Zone Health.
 *
 * Both read the same /api/analytics/exposure payload (shared React Query key, so
 * one deduped request feeds both cards). Values come from the backend analytics
 * service — worst open-finding severity per protocol, and 100−avg-burden per
 * network zone — so these are real, not the old static mock numbers.
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Activity, Shield } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { ProtocolRow } from "./ProtocolRow";
import { ZoneRow } from "./ZoneRow";

interface Exposure {
  protocols: { name: string; value: number }[];
  zones: { name: string; score: number }[];
}

function useExposure() {
  return useQuery({
    queryKey: ["exposure"],
    queryFn: () => fetchJson<Exposure>("/api/analytics/exposure"),
    refetchInterval: 60_000,
  });
}

export function ProtocolRiskCard() {
  const { data, isLoading, error, refetch } = useExposure();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={38} /></div>;
  if (error) return <ErrorState title="Couldn't load protocol risk." onRetry={() => refetch()} />;
  const protocols = data?.protocols ?? [];
  if (protocols.length === 0) {
    return <div style={{ padding: 24 }}><EmptyState icon={Activity} title="No exposed services yet" hint="Protocol risk appears once discovery finds services on your assets." /></div>;
  }
  return (
    <>
      {protocols.map((p, i) => (
        <ProtocolRow key={p.name} protocol={p} isLast={i === protocols.length - 1} />
      ))}
    </>
  );
}

export function ZoneHealthCard() {
  const { data, isLoading, error, refetch } = useExposure();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={38} /></div>;
  if (error) return <ErrorState title="Couldn't load zone health." onRetry={() => refetch()} />;
  const zones = data?.zones ?? [];
  if (zones.length === 0) {
    return <div style={{ padding: 24 }}><EmptyState icon={Shield} title="No zones yet" hint="Zone health appears once assets are tagged with an environment." /></div>;
  }
  return (
    <>
      {zones.map((z, i) => (
        <ZoneRow key={z.name} zone={z} isLast={i === zones.length - 1} />
      ))}
    </>
  );
}
