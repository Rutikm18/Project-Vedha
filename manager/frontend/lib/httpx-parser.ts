export interface HttpxJsonRecord {
  url: string;
  host?: string;
  port?: number;
  status_code?: number;
  title?: string;
  tech?: string[];
  webserver?: string;
  scheme?: string;
}

export type HttpxLineParseResult =
  | { ok: true; record: HttpxJsonRecord }
  | { ok: false; reason: 'invalid_json' | 'invalid_record' };

function isOptionalString(value: unknown): value is string | undefined {
  return value === undefined || typeof value === 'string';
}

function normalizePort(value: unknown): number | undefined | null {
  if (value === undefined) return undefined;

  const port = typeof value === 'string' && /^\d+$/.test(value)
    ? Number(value)
    : value;
  if (
    typeof port !== 'number'
    || !Number.isInteger(port)
    || port < 1
    || port > 65535
  ) {
    return null;
  }
  return port;
}

function isOptionalNumber(value: unknown): value is number | undefined {
  return value === undefined || (typeof value === 'number' && Number.isFinite(value));
}

export function parseHttpxJsonLine(line: string): HttpxLineParseResult {
  let value: unknown;
  try {
    value = JSON.parse(line);
  } catch {
    return { ok: false, reason: 'invalid_json' };
  }

  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    return { ok: false, reason: 'invalid_record' };
  }

  const record = value as Record<string, unknown>;
  const port = normalizePort(record.port);
  const tech = record.tech === undefined
    ? undefined
    : Array.isArray(record.tech) && record.tech.every((item) => typeof item === 'string')
      ? record.tech as string[]
      : null;
  if (
    typeof record.url !== 'string'
    || record.url.trim().length === 0
    || !isOptionalString(record.host)
    || port === null
    || !isOptionalNumber(record.status_code)
    || !isOptionalString(record.title)
    || !isOptionalString(record.webserver)
    || !isOptionalString(record.scheme)
    || tech === null
  ) {
    return { ok: false, reason: 'invalid_record' };
  }

  return {
    ok: true,
    record: {
      url: record.url.trim(),
      host: record.host,
      port,
      status_code: record.status_code,
      title: record.title,
      tech,
      webserver: record.webserver,
      scheme: record.scheme,
    },
  };
}

/**
 * Incrementally decodes HTTPX JSONL without losing the final line when stdout
 * does not end with a newline.
 */
export class HttpxJsonlDecoder {
  private buffer = '';

  invalidJsonLines = 0;
  invalidRecordLines = 0;

  push(chunk: string): HttpxJsonRecord[] {
    this.buffer += chunk;
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() ?? '';
    return this.decode(lines);
  }

  finish(): HttpxJsonRecord[] {
    const finalLine = this.buffer;
    this.buffer = '';
    return this.decode(finalLine ? [finalLine] : []);
  }

  get malformedLines(): number {
    return this.invalidJsonLines + this.invalidRecordLines;
  }

  private decode(lines: string[]): HttpxJsonRecord[] {
    const records: HttpxJsonRecord[] = [];

    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line) continue;

      const parsed = parseHttpxJsonLine(line);
      if (parsed.ok === false) {
        if (parsed.reason === 'invalid_json') this.invalidJsonLines += 1;
        else this.invalidRecordLines += 1;
        continue;
      }
      records.push(parsed.record);
    }

    return records;
  }
}
