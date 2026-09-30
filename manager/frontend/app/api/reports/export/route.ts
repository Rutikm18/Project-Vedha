import { NextResponse } from "next/server";

import { backend } from "../../../../lib/backend";
import {
  buildReportExport,
  type ReportExportFormat,
} from "../../../../lib/report/export-files";
import type { ReportDocument } from "../../../../lib/report/report-document";
import { withBackend } from "../../../../lib/with-backend";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

const FORMATS = new Set<ReportExportFormat>(["csv", "xlsx", "pdf", "docx"]);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const ALLOWED_KEYS = new Set(["format", "engagementId"]);

interface ExportBody {
  format: ReportExportFormat;
  engagementId: string;
}

function parseBody(value: unknown): ExportBody | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const body = value as Record<string, unknown>;
  if (Object.keys(body).some((key) => !ALLOWED_KEYS.has(key))) return null;
  if (typeof body.format !== "string" || !FORMATS.has(body.format as ReportExportFormat)) return null;
  if (typeof body.engagementId !== "string" || !UUID.test(body.engagementId)) return null;
  return body as unknown as ExportBody;
}

function attachment(filename: string): string {
  const ascii = filename.replace(/[^a-zA-Z0-9._-]/g, "-");
  return `attachment; filename="${ascii}"; filename*=UTF-8''${encodeURIComponent(filename)}`;
}

export const POST = withBackend(async (request, { token }): Promise<Response> => {
  const body = parseBody(await request.json().catch(() => null));
  if (!body) {
    return NextResponse.json(
      { error: "Body must contain only a valid engagementId and export format." },
      { status: 400 },
    );
  }

  const report = await backend<ReportDocument>(
    `/engagements/${encodeURIComponent(body.engagementId)}/report-document`,
    { token },
  );
  const file = await buildReportExport(body.format, report);
  return new Response(new Uint8Array(file.bytes), {
    status: 200,
    headers: {
      "Content-Type": file.contentType,
      "Content-Disposition": attachment(file.filename),
      "Content-Length": String(file.bytes.length),
      "Cache-Control": "private, no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
});
