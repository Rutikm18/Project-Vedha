/**
 * download.ts — authenticated file downloads for the report exports.
 *
 * A bare <a href download> saves whatever comes back: on an expired session or
 * a server error the "report" the user emails is a JSON error body. Fetching
 * first lets us refresh the session once, surface a real error, and name the
 * file from the server's Content-Disposition.
 */

export type DownloadSurface = "manager" | "portal";

/** filename="x.xlsx" / filename*=UTF-8''x.xlsx → "x.xlsx"; null when absent. */
export function filenameFromDisposition(header: string | null): string | null {
  if (!header) return null;
  const star = header.match(/filename\*\s*=\s*(?:UTF-8'')?([^;]+)/i);
  if (star) {
    try { return decodeURIComponent(star[1].trim().replace(/^"|"$/g, "")); } catch { /* fall through */ }
  }
  const plain = header.match(/filename\s*=\s*"([^"]+)"|filename\s*=\s*([^;]+)/i);
  const name = plain ? (plain[1] ?? plain[2]).trim() : "";
  return name || null;
}

export function saveBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function errorDetail(res: Response): Promise<string> {
  try {
    const body = await res.json();
    const d = body?.detail ?? body?.error ?? body?.message;
    if (typeof d === "string" && d) return d;
  } catch { /* non-JSON */ }
  return `Export failed (${res.status}).`;
}

/** GET `url` and save it; throws an Error with a readable message on failure. */
export async function downloadFile(url: string, surface: DownloadSurface, fallbackName: string): Promise<void> {
  const get = () => fetch(url, { credentials: "same-origin" });
  let res: Response;
  try {
    res = await get();
    if (res.status === 401) {
      const refresh = await fetch(surface === "portal" ? "/api/portal/login" : "/api/auth/login", {
        method: "PUT", credentials: "same-origin",
      });
      if (refresh.ok) res = await get();
    }
  } catch {
    throw new Error("Can't reach the server. Check your connection and try again.");
  }
  if (res.status === 401) throw new Error("Your session has expired. Sign in again, then retry the export.");
  if (!res.ok) throw new Error(await errorDetail(res));
  const name = filenameFromDisposition(res.headers.get("content-disposition")) ?? fallbackName;
  saveBlob(await res.blob(), name);
}
