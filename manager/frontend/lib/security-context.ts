import { backend, BackendError } from "./backend";
import { toUiFinding } from "./adapters";
import { cveRecordToFactCard, detectFindingId, toFactCard, type FactCardVM } from "./assistant";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CVE = /^CVE-\d{4}-\d{4,7}$/i;
const MAX_CVE_RESPONSE_BYTES = 1_000_000;

export class SecurityContextError extends Error {
  status: number;
  constructor(message: string, status = 502) {
    super(message);
    this.name = "SecurityContextError";
    this.status = status;
  }
}

async function publicCveRecord(cveId: string, fetchImpl: typeof fetch): Promise<unknown> {
  const response = await fetchImpl(`https://cveawg.mitre.org/api/cve/${encodeURIComponent(cveId)}`, {
    headers: { Accept: "application/json" },
    cache: "no-store",
    signal: AbortSignal.timeout(8_000),
  });
  if (response.status === 404) throw new SecurityContextError(`${cveId} is not a published CVE record`, 404);
  if (!response.ok) throw new SecurityContextError(`The public CVE service returned ${response.status}`, 502);
  const declaredSize = Number(response.headers.get("content-length") ?? 0);
  if (declaredSize > MAX_CVE_RESPONSE_BYTES) throw new SecurityContextError("The CVE record exceeded the safe response limit", 502);
  const text = await response.text();
  if (text.length > MAX_CVE_RESPONSE_BYTES) throw new SecurityContextError("The CVE record exceeded the safe response limit", 502);
  try {
    return JSON.parse(text);
  } catch {
    throw new SecurityContextError("The public CVE service returned invalid JSON", 502);
  }
}

export async function resolveSecurityReference({
  reference,
  token,
  fetchImpl = fetch,
}: {
  reference: string;
  token: string;
  fetchImpl?: typeof fetch;
}): Promise<{ factCard: FactCardVM; finding: any | null }> {
  const detected = detectFindingId(reference) ?? reference.trim();
  if (UUID.test(detected)) {
    const raw = await backend<any>(`/findings/${encodeURIComponent(detected)}`, { token });
    const finding = toUiFinding(raw);
    return { factCard: toFactCard(finding), finding };
  }
  if (!CVE.test(detected)) throw new SecurityContextError("Enter a valid finding UUID or CVE identifier", 400);

  const cveId = detected.toUpperCase();
  try {
    const result = await backend<{ items?: any[] }>("/findings", {
      token,
      query: { search: cveId, page: 1, page_size: 100, sort: "risk" },
    });
    const exact = (result.items ?? []).find((finding) =>
      Array.isArray(finding.cve_ids)
      && finding.cve_ids.some((value: unknown) => String(value).toUpperCase() === cveId),
    );
    if (exact) {
      const finding = toUiFinding(exact);
      return { factCard: toFactCard(finding), finding };
    }
  } catch (error) {
    if (error instanceof BackendError) throw error;
    throw new SecurityContextError("Vedha finding lookup failed", 502);
  }

  const record = await publicCveRecord(cveId, fetchImpl);
  return { factCard: cveRecordToFactCard(record, cveId), finding: null };
}
