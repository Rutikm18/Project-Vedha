import fs   from 'fs';
import path from 'path';
import os   from 'os';

const SESSION_DIR  = path.join(os.homedir(), '.vedha');
const SESSION_FILE = path.join(SESSION_DIR, 'session.json');

export interface Session {
  email:     string;
  token:     string;
  role:      string;
  savedAt:   string;
  /** Id of the personal access token in `token`, so logout can revoke it. */
  patId?:    string;
}

export function loadSession(): Session | null {
  try {
    if (!fs.existsSync(SESSION_FILE)) return null;
    return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf-8')) as Session;
  } catch {
    return null;
  }
}

export function saveSession(session: Session): void {
  if (!fs.existsSync(SESSION_DIR)) fs.mkdirSync(SESSION_DIR, { recursive: true, mode: 0o700 });
  fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2), { mode: 0o600 });
}

export function clearSession(): void {
  try { fs.unlinkSync(SESSION_FILE); } catch { /* already gone */ }
}

export function requireAuth(): Session {
  const s = loadSession();
  if (!s) {
    process.stderr.write('\x1b[1;31m[ERR]\x1b[0m Not authenticated. Run: vedha login\n');
    process.exit(1);
  }
  return s;
}

export function serverUrl(): string {
  return process.env.VEDHA_SERVER ?? 'http://localhost:3000';
}

export async function apiFetch(
  session: Session,
  endpoint: string,
  opts?: RequestInit,
): Promise<Response> {
  return fetch(`${serverUrl()}${endpoint}`, {
    ...opts,
    headers: {
      'Content-Type':  'application/json',
      'Authorization': `Bearer ${session.token}`,
      ...(opts?.headers ?? {}),
    },
  });
}

// ── Password login ───────────────────────────────────────────────────────────
// The CLI signs in like the dashboard (email + password through the BFF), then
// swaps the short-lived browser session for a personal access token: revocable,
// 30 days, and unable to mint further tokens. Only the token is stored.

export class LoginError extends Error {
  constructor(message: string, readonly unreachable = false) { super(message); }
}

const CLI_TOKEN_DAYS = 30;

/** Value of a cookie set by a response, or null. */
export function setCookieValue(setCookies: string[], name: string): string | null {
  for (const line of setCookies) {
    const first = line.split(';', 1)[0].trim();
    if (first.startsWith(`${name}=`)) {
      const raw = first.slice(name.length + 1);
      try { return decodeURIComponent(raw); } catch { return raw; }
    }
  }
  return null;
}

export async function loginWithPassword(
  server: string,
  email: string,
  password: string,
): Promise<Session> {
  const json = { 'Content-Type': 'application/json' };

  const res = await fetch(`${server}/api/auth/login`, {
    method: 'POST', headers: json, body: JSON.stringify({ email, password }),
  }).catch(() => null);
  if (!res) throw new LoginError(`Could not reach the VEDHA server at ${server}.`, true);
  if (!res.ok) {
    const body = await res.json().catch(() => ({})) as { error?: string; code?: string };
    throw new LoginError(
      body.code === 'invalid_credentials' ? 'Invalid email or password.'
      : body.code === 'rate_limited'      ? 'Too many attempts. Wait a minute and try again.'
      : body.error ?? `Login failed (HTTP ${res.status}).`,
    );
  }

  const cookies = res.headers.getSetCookie();
  const access  = setCookieValue(cookies, 'vedha_token');
  const refresh = setCookieValue(cookies, 'vedha_refresh_token');
  if (!access) throw new LoginError('The server did not start a session.');

  const patRes = await fetch(`${server}/api/auth/pats`, {
    method: 'POST',
    headers: { ...json, Authorization: `Bearer ${access}` },
    body: JSON.stringify({
      name: `vedha-cli (${os.hostname()})`,
      scopes: ['api:read', 'api:write'],
      expires_in_days: CLI_TOKEN_DAYS,
    }),
  }).catch(() => null);

  // The browser-style refresh token is not needed once we hold a PAT: revoke it
  // so no unused credential outlives the login.
  if (refresh) {
    await fetch(`${server}/api/auth/login`, {
      method: 'DELETE', headers: { Cookie: `vedha_refresh_token=${encodeURIComponent(refresh)}` },
    }).catch(() => null);
  }

  if (!patRes?.ok) {
    throw new LoginError('Signed in, but the server would not issue a CLI token.');
  }
  const pat = await patRes.json() as { id: string; token: string };

  const meRes = await fetch(`${server}/api/auth/me`, {
    headers: { Authorization: `Bearer ${pat.token}` },
  }).catch(() => null);
  const me = meRes?.ok ? await meRes.json() as { email?: string; role?: string } : {};

  return {
    email:   me.email ?? email,
    token:   pat.token,
    role:    me.role ?? 'operator',
    savedAt: new Date().toISOString(),
    patId:   pat.id,
  };
}

/** Best-effort server-side revocation of the CLI token (logout). */
export async function revokeSessionToken(session: Session, server: string = serverUrl()): Promise<void> {
  if (!session.patId) return;
  await fetch(`${server}/api/auth/pats/${encodeURIComponent(session.patId)}`, {
    method: 'DELETE', headers: { Authorization: `Bearer ${session.token}` },
  }).catch(() => null);
}
