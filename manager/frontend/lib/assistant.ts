// Ask Vedha — pure logic shared by the assistant drawer and the explain BFF route.
// Grounded by design: everything here maps REAL finding fields; nothing is invented.

export type FactCardVM = {
  id: string; title: string; severity: string;
  whatItIs: string; whyItMatters: string; whatToDo: string;
  cvss: string; epssPct: number; risk: number;
  kev: boolean; exploited: boolean; status: string; host: string;
  cveIds: string[];
  source: "finding" | "cve";
  sourceLabel: string;
  sourceUrl?: string;
  affectedAssets: string[];
  remediationSteps: string[];
  references: Array<{ label: string; url: string }>;
  evidenceStatus: string;
};

const UUID_RE = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;
const CVE_RE = /CVE-\d{4}-\d{4,7}/i;

/** Pull a finding id (UUID) or a CVE id out of free text. Returns null if neither is present. */
export function detectFindingId(text: string): string | null {
  const uuid = text.match(UUID_RE);
  if (uuid) return uuid[0].toLowerCase();
  const cve = text.match(CVE_RE);
  if (cve) return cve[0].toUpperCase();
  return null;
}

function isExploited(f: any): boolean {
  return Boolean(f.activelyExploited ?? f.exploitable);
}

function plainWhyItMatters(f: any): string {
  const bits: string[] = [];
  if (isExploited(f)) bits.push("attackers are actively exploiting this in the wild");
  if (f.kevListed) bits.push("it is on CISA's Known Exploited Vulnerabilities list");
  const epssPct = Math.round((f.epssScore ?? 0) * 100);
  if (epssPct >= 10) bits.push(`there is a ${epssPct}% modelled chance of exploitation (EPSS)`);
  if (bits.length === 0) bits.push(`it carries a ${String(f.severity ?? "info").toLowerCase()} severity rating`);
  return `This matters because ${bits.join(", and ")}.`;
}

/** Build the deterministic fact card from a UI finding (output of lib/adapters.toUiFinding). */
export function toFactCard(f: any): FactCardVM {
  const rem = Array.isArray(f.remediation) ? f.remediation : [];
  const remediationSteps = rem.map((step: unknown) => {
    if (typeof step === "string") return step.trim();
    if (!step || typeof step !== "object") return "";
    const value = step as { title?: unknown; description?: unknown };
    return String(value.description ?? value.title ?? "").trim();
  }).filter(Boolean);
  const cveIds = [...new Set(
    [...(Array.isArray(f.cves) ? f.cves : []), ...(Array.isArray(f.tags) ? f.tags : [])]
      .map((value) => String(value).toUpperCase())
      .filter((value) => /^CVE-\d{4}-\d{4,7}$/.test(value)),
  )];
  const host = f.affectedHost ?? "—";
  const impact = String(f.businessImpact ?? f.impact ?? "").trim();
  return {
    id: String(f.id),
    title: f.title ?? "Untitled finding",
    severity: String(f.severity ?? "INFO"),
    whatItIs: String(f.description ?? "").trim()
      || `${f.title ?? "This finding"}${f.category ? ` — a ${f.category} issue` : ""} on ${host}.`,
    whyItMatters: impact || plainWhyItMatters(f),
    whatToDo: remediationSteps[0] ?? "No remediation has been recorded. Assign an owner to validate the issue and document a safe corrective action.",
    cvss: f.cvss != null ? String(f.cvss) : "—",
    epssPct: Math.round((f.epssScore ?? 0) * 100),
    risk: Math.round(f.riskScore ?? 0),
    kev: Boolean(f.kevListed),
    exploited: isExploited(f),
    status: String(f.status ?? "OPEN"),
    host,
    cveIds,
    source: "finding",
    sourceLabel: "Vedha recorded finding",
    affectedAssets: host && host !== "—" ? [host] : [],
    remediationSteps,
    references: cveIds.map((id) => ({ label: `${id} · CVE Program`, url: `https://www.cve.org/CVERecord?id=${id}` })),
    evidenceStatus: "Organization impact is based on a tenant-authorized Vedha finding.",
  };
}

function preferredText(values: unknown): string {
  if (!Array.isArray(values)) return "";
  const entries = values as Array<{ lang?: string; value?: string }>;
  return (entries.find((entry) => entry.lang === "en") ?? entries[0])?.value?.trim() ?? "";
}

function publicSeverity(score: number | null, fallback: string): string {
  const normalized = fallback.toUpperCase();
  if (["CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"].includes(normalized)) return normalized;
  if (score == null) return "UNKNOWN";
  if (score >= 9) return "CRITICAL";
  if (score >= 7) return "HIGH";
  if (score >= 4) return "MEDIUM";
  if (score > 0) return "LOW";
  return "NONE";
}

/** Convert a CVE JSON 5 record into the same deterministic customer brief used for findings. */
export function cveRecordToFactCard(record: any, requestedId: string): FactCardVM {
  const id = String(record?.cveMetadata?.cveId ?? requestedId).toUpperCase();
  const cna = record?.containers?.cna ?? {};
  const adp = Array.isArray(record?.containers?.adp) ? record.containers.adp : [];
  const containers = [cna, ...adp];
  const metrics = containers.flatMap((container) => Array.isArray(container?.metrics) ? container.metrics : []);
  let cvss: number | null = null;
  let severity = "";
  for (const metric of metrics) {
    for (const key of ["cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"]) {
      const value = metric?.[key];
      const score = Number(value?.baseScore);
      if (Number.isFinite(score)) {
        cvss = score;
        severity = String(value?.baseSeverity ?? "");
        break;
      }
    }
    if (cvss != null) break;
    const other = String(metric?.other?.content?.other ?? "");
    if (other) severity = other;
  }
  const description = preferredText(cna.descriptions) || "The published CVE record does not contain an English description.";
  const affected = Array.isArray(cna.affected) ? cna.affected : [];
  const products = [...new Set(affected.map((entry: any) =>
    [entry?.vendor, entry?.product].filter(Boolean).join(" "),
  ).filter(Boolean))].slice(0, 8);
  const solutionText = [
    ...(Array.isArray(cna.solutions) ? cna.solutions : []),
    ...(Array.isArray(cna.workarounds) ? cna.workarounds : []),
  ].map((entry: any) => String(entry?.value ?? "").trim()).filter(Boolean);
  const remediationSteps = solutionText.length ? solutionText.slice(0, 5) : [
    "Confirm whether the named product and an affected version exist in the authorized asset inventory.",
    "Review the vendor advisory and apply the vendor-fixed release or documented mitigation.",
    "Retest the affected service and preserve evidence before closing the risk.",
  ];
  const references = containers
    .flatMap((container) => Array.isArray(container?.references) ? container.references : [])
    .map((reference: any) => ({ label: String(reference?.name ?? "Vendor or CVE reference"), url: String(reference?.url ?? "") }))
    .filter((reference) => /^https?:\/\//i.test(reference.url))
    .filter((reference, index, all) => all.findIndex((item) => item.url === reference.url) === index)
    .slice(0, 6);
  const scoreLabel = cvss == null ? "—" : String(cvss);
  const normalizedSeverity = publicSeverity(cvss, severity);

  return {
    id,
    title: id,
    severity: normalizedSeverity,
    whatItIs: description,
    whyItMatters: products.length
      ? `This vulnerability affects ${products.join(", ")}. Vedha has not confirmed that these products are present in the organization.`
      : "Organizational impact is unknown until the affected product, version, exposure, and business criticality are validated.",
    whatToDo: remediationSteps[0],
    cvss: scoreLabel,
    epssPct: 0,
    risk: 0,
    kev: false,
    exploited: false,
    status: String(record?.cveMetadata?.state ?? "PUBLISHED"),
    host: "Not validated",
    cveIds: [id],
    source: "cve",
    sourceLabel: "Public CVE Program record",
    sourceUrl: `https://www.cve.org/CVERecord?id=${id}`,
    affectedAssets: [],
    remediationSteps,
    references: [
      { label: `${id} · CVE Program`, url: `https://www.cve.org/CVERecord?id=${id}` },
      ...references,
    ].filter((reference, index, all) => all.findIndex((item) => item.url === reference.url) === index),
    evidenceStatus: "Public vulnerability metadata only. This is not evidence that the organization is affected.",
  };
}
