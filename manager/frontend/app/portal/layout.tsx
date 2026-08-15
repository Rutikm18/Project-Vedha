/**
 * Portal segment layout — a passthrough. Each portal page renders its own
 * <PortalShell title=…> (mirroring how operator pages use <PageShell>), so the
 * shell can carry a per-page title/subtitle. The login screen renders standalone.
 */
export default function PortalLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
