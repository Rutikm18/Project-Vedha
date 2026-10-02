"use client";

/**
 * Fleet → Add agent. One panel for the operator console and the customer portal.
 *
 * The flow mirrors how Tenable / Qualys onboard a scanner: pick what the agent is
 * for (the portal's engagement is implicit), get ONE command with a single-use
 * install token, run it on a Linux host with Docker, and watch it connect. The
 * manager serves the signed agent itself, so nothing is pulled from a public
 * registry and the only firewall rule a customer needs is HTTPS to the manager.
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  AlertTriangle, Ban, CheckCircle2, ChevronDown, Clipboard, KeyRound, Loader2, ShieldCheck,
} from "lucide-react";
import { formatExact } from "../../components/portal/Timestamp";
import { useToast } from "../../hooks/useToast";
import { copyText } from "../../lib/clipboard";
import { INSTALL_LIFETIMES } from "../../lib/fleet-workspace-api";
import type {
  AgentInstallInfo, FleetEngagementOption, FleetWorkspaceSurface, InstallToken,
  createFleetWorkspaceApi,
} from "../../lib/fleet-workspace-api";

type FleetApi = ReturnType<typeof createFleetWorkspaceApi>;

const STATE_COLOR: Record<InstallToken["state"], string> = {
  active: "var(--sev-medium-color)",
  used: "var(--nominal-color)",
  expired: "var(--text-faint)",
  revoked: "var(--text-faint)",
};

const STATE_LABEL: Record<InstallToken["state"], string> = {
  active: "waiting for install",
  used: "agent enrolled",
  expired: "expired",
  revoked: "revoked",
};

/** Host the agent dials, for the requirement line ("outbound HTTPS to …"). */
export function managerHost(url: string): string {
  try {
    const parsed = new URL(url);
    return parsed.port ? `${parsed.hostname}:${parsed.port}` : parsed.hostname;
  } catch {
    return url || "your Vedha manager";
  }
}

export default function AddAgent({ surface, api }: { surface: FleetWorkspaceSurface; api: FleetApi }) {
  const toast = useToast();
  const [info, setInfo] = useState<AgentInstallInfo | null>(null);
  const [engagements, setEngagements] = useState<FleetEngagementOption[]>([]);
  const [engagementId, setEngagementId] = useState("");
  const [name, setName] = useState("");
  const [lifetime, setLifetime] = useState(24 * 60);
  const [tokens, setTokens] = useState<InstallToken[]>([]);
  const [created, setCreated] = useState<InstallToken | null>(null);
  const [busy, setBusy] = useState(false);
  const [showInspect, setShowInspect] = useState(false);
  const [showReqs, setShowReqs] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTokens = useCallback(async () => {
    try {
      setTokens(await api.installTokens(surface === "manager" ? engagementId || undefined : undefined));
    } catch { /* keep the last list on a transient failure */ }
  }, [api, surface, engagementId]);

  useEffect(() => {
    let alive = true;
    void (async () => {
      try {
        const [nextInfo, nextEngagements] = await Promise.all([
          api.installInfo(),
          api.engagements().catch(() => [] as FleetEngagementOption[]),
        ]);
        if (!alive) return;
        setInfo(nextInfo);
        const open = nextEngagements.filter((e) => !["COMPLETED", "ARCHIVED"].includes(String(e.status).toUpperCase()));
        setEngagements(open);
        setEngagementId((current) => current || (open.length === 1 ? open[0].id : ""));
      } catch (error) {
        if (alive) setInfo({ available: false, reason: error instanceof Error ? error.message : "Could not load the agent installer status", manager_url: "", manager_url_configured: false });
      }
    })();
    return () => { alive = false; };
  }, [api]);

  // Poll the token list so "waiting for install" turns into "agent enrolled"
  // on its own while the customer runs the command.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- mount fetch + 5s poll; setState happens after an await
    void loadTokens();
    const timer = window.setInterval(() => void loadTokens(), 5000);
    return () => window.clearInterval(timer);
  }, [loadTokens]);

  const createdState = useMemo(
    () => (created ? tokens.find((t) => t.id === created.id)?.state ?? created.state : null),
    [created, tokens],
  );

  const copy = (text: string) =>
    void copyText(text).then((ok) => (
      ok ? toast.success("Command copied") : toast.error("Copy failed — select the command and copy it manually")
    ));

  async function generate(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const token = await api.createInstallToken(surface === "manager" ? engagementId || null : null, name.trim(), lifetime);
      setCreated(token);
      setShowInspect(false);
      toast.success("Install command ready — it works once and expires in 24 hours");
      await loadTokens();
    } catch (err) {
      // Inline as well as a toast: a blocking reason ("already has an agent")
      // must stay readable until the operator changes something.
      const message = err instanceof Error ? err.message : "Could not create the install command";
      setError(message);
      toast.error(message);
    } finally {
      setBusy(false);
    }
  }

  async function revoke(id: string) {
    try {
      await api.revokeInstallToken(id);
      if (created?.id === id) setCreated(null);
      toast.success("Install command revoked");
      await loadTokens();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Could not revoke the install command");
    }
  }

  const host = managerHost(info?.manager_url ?? "");
  const blocked = surface === "portal" && info?.can_add_agent === false;
  const canGenerate = Boolean(info?.available) && !blocked && (surface === "portal" || Boolean(engagementId));
  const recent = tokens.filter((t) => t.id !== created?.id).slice(0, 6);

  return (
    <section className="flt-card" aria-labelledby="add-agent-title">
      <div className="flt-card-head">
        <span className="flt-head-icon"><ShieldCheck size={17} /></span>
        <div>
          <strong id="add-agent-title" className="flt-head-title">Add a vedha-agent</strong>
          <div className="flt-head-sub">
            Runs on a Linux host with Docker inside the network you want assessed. It only connects
            out to <span className="flt-mono">{host}</span> over HTTPS — no inbound ports.
          </div>
        </div>
      </div>

      {info === null ? (
        <div className="flt-empty"><Loader2 size={15} className="animate-spin" /> Checking the agent installer…</div>
      ) : !info.available ? (
        <div className="aa-note aa-warn" role="status">
          <AlertTriangle size={14} />
          <div>
            <strong>The agent installer is not available yet.</strong>
            {surface === "manager" ? (
              <>
                {" "}{info.reason}. Publish a signed release from the build machine:{" "}
                <span className="flt-mono">make agent-release</span> then{" "}
                <span className="flt-mono">make agent-publish TO=…</span> and set{" "}
                <span className="flt-mono">AGENT_RELEASE_PUBLIC_KEY</span> on the manager.
              </>
            ) : " Your Vedha team needs to publish it — contact them, then come back to this page."}
          </div>
        </div>
      ) : (
        <div className="aa-release" aria-label="Agent release">
          <CheckCircle2 size={13} color="var(--nominal-color)" />
          <span>Agent <strong className="flt-mono">{info.version}</strong></span>
          <span className="aa-dot">·</span>
          <span>{(info.arches ?? []).join(", ")}</span>
          <span className="aa-dot">·</span>
          <span>{info.signed ? <>signed <span className="flt-mono">({info.signing_key_id})</span></> : "unsigned (development)"}</span>
        </div>
      )}

      {surface === "manager" && info && !info.manager_url_configured && (
        <p className="flt-warn">MANAGER_PUBLIC_URL is not set on the API, so commands use {info.manager_url || "this request's address"}. Set it to the public API URL (for example https://api.your-domain.com).</p>
      )}
      {blocked && info?.blocker && (
        <div className="aa-note" role="status"><AlertTriangle size={14} /><div>{info.blocker}.</div></div>
      )}

      <form className="aa-form" onSubmit={generate}>
        {surface === "manager" && (
          <label className="flt-field">
            <span className="flt-label">Engagement <span className="flt-req-star" aria-hidden="true">*</span></span>
            <select
              className="flt-input"
              required
              value={engagementId}
              onChange={(e) => { setEngagementId(e.target.value); setCreated(null); setError(null); }}
            >
              <option value="">Choose the engagement this agent scans for…</option>
              {engagements.map((e) => (
                <option key={e.id} value={e.id}>{e.name} ({e.scopeCidrs.length} scope range{e.scopeCidrs.length === 1 ? "" : "s"})</option>
              ))}
            </select>
            <span className="flt-hint">The agent gets exactly this engagement&apos;s scope when it enrols.</span>
          </label>
        )}
        <label className="flt-field">
          <span className="flt-label">Label <span className="flt-optional">(optional)</span></span>
          <input
            className="flt-input"
            maxLength={120}
            placeholder="e.g. Mumbai office VM"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <label className="flt-field">
          <span className="flt-label">Command valid for</span>
          <select
            className="flt-input"
            value={lifetime}
            onChange={(e) => setLifetime(Number(e.target.value))}
          >
            {INSTALL_LIFETIMES.map((l) => (
              <option key={l.minutes} value={l.minutes}>{l.label}</option>
            ))}
          </select>
          <span className="flt-hint">How long the command works before it expires. It is single-use either way.</span>
        </label>
        <button className="flt-submit aa-submit" type="submit" disabled={!canGenerate || busy}>
          {busy ? <Loader2 size={15} className="animate-spin" /> : <KeyRound size={15} />} Generate install command
        </button>
      </form>

      {error && (
        <div className="aa-note aa-warn" role="alert"><AlertTriangle size={14} /><div>{error}</div></div>
      )}

      {created?.commands && (
        <div className="aa-result" aria-live="polite">
          <div className="aa-result-head">
            <span className="flt-cmd-label">Run on the Linux host (as root)</span>
            <span className="flt-state" style={{ color: STATE_COLOR[createdState ?? "active"] }}>
              <span className="flt-dot" style={{ background: STATE_COLOR[createdState ?? "active"] }} />
              {STATE_LABEL[createdState ?? "active"]}
            </span>
          </div>
          <div className="flt-install">
            <code className="flt-code">{created.commands.one_line}</code>
            <button className="flt-icon-btn" aria-label="Copy install command" onClick={() => copy(created.commands!.one_line)}>
              <Clipboard size={15} />
            </button>
          </div>
          <p className="aa-small">
            Works once, until {formatExact(created.expires_at)}. Anyone holding it can add an agent to
            this engagement until then — share it only with the person installing, or revoke it below.
            {createdState === "used" && " The agent has enrolled; it appears under Connected vedha-agents."}
          </p>
          <button type="button" className="aa-link" onClick={() => setShowInspect((v) => !v)} aria-expanded={showInspect}>
            <ChevronDown size={12} className="flt-chev" data-open={showInspect} /> Prefer to read the installer first?
          </button>
          {showInspect && (
            <div className="flt-cmds">
              {(["download", "run"] as const).map((key, index) => (
                <div className="flt-cmd" key={key}>
                  <span className="flt-cmd-label">{index + 1}. {key === "download" ? "Download, then read vedha-install.sh" : "Run it"}</span>
                  <div className="flt-install">
                    <code className="flt-code">{created.commands![key]}</code>
                    <button className="flt-icon-btn" aria-label={`Copy ${key} command`} onClick={() => copy(created.commands![key])}>
                      <Clipboard size={15} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <button type="button" className="aa-link" onClick={() => setShowReqs((v) => !v)} aria-expanded={showReqs}>
        <ChevronDown size={12} className="flt-chev" data-open={showReqs} /> Host requirements and network checklist
      </button>
      {showReqs && (
        <ul className="aa-reqs">
          <li><strong>Host:</strong> Linux VM or server (Ubuntu 22.04+, Debian 12, RHEL 9, Amazon Linux 2023), amd64 or arm64, 2 vCPU · 4 GB RAM · 20 GB disk, Docker Engine.</li>
          <li><strong>Placement:</strong> on the same network segment as the systems in scope, with a fixed IP (DHCP reservation).</li>
          <li><strong>Network:</strong> outbound HTTPS (443) to <span className="flt-mono">{host}</span>; DNS that resolves it; working time sync (NTP).</li>
          <li><strong>Proxy:</strong> add <span className="flt-mono">--proxy http://proxy:3128</span> to the command. A TLS-inspecting proxy also needs <span className="flt-mono">--ca-bundle /path/ca.pem</span>, or an inspection exemption for the manager.</li>
          <li><strong>Security tools:</strong> allow-list the agent&apos;s IP in IPS/NAC so scans aren&apos;t blocked mid-way; tell your SOC before the first scan.</li>
          <li><strong>Integrity:</strong> the installer verifies the release signature (OpenSSL 3) and the image checksum before running anything.</li>
        </ul>
      )}

      {recent.length > 0 && (
        <div className="aa-tokens">
          <span className="flt-cmd-label">Recent install commands</span>
          {recent.map((t) => (
            <div className="aa-token" key={t.id}>
              <span className="flt-mono">{t.token_prefix}…</span>
              <span className="aa-token-name">{t.name}</span>
              <span className="flt-state" style={{ color: STATE_COLOR[t.state] }}>
                <span className="flt-dot" style={{ background: STATE_COLOR[t.state] }} />{STATE_LABEL[t.state]}
              </span>
              <span className="aa-token-time">{t.state === "used" ? formatExact(t.last_used_at) : `until ${formatExact(t.expires_at)}`}</span>
              {t.state === "active" && (
                <button type="button" className="aa-revoke" onClick={() => void revoke(t.id)} aria-label={`Revoke install command ${t.token_prefix}`}>
                  <Ban size={12} /> Revoke
                </button>
              )}
            </div>
          ))}
        </div>
      )}
      {created && createdState === "active" && (
        <button type="button" className="aa-revoke aa-revoke-current" onClick={() => void revoke(created.id)}>
          <Ban size={12} /> Revoke this command
        </button>
      )}
    </section>
  );
}

export const ADD_AGENT_STYLES = `
.aa-release { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; color: var(--text-secondary); font-size: 11.5px; margin-bottom: 12px; }
.aa-dot { color: var(--text-faint); }
.aa-note { display: flex; gap: 8px; align-items: flex-start; padding: 10px 12px; border-radius: 8px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); font-size: 11.5px; line-height: 1.5; margin-bottom: 12px; }
.aa-note svg { flex-shrink: 0; margin-top: 2px; color: var(--sev-medium-color); }
.aa-warn { border-color: var(--sev-medium-color); }
.aa-form + .aa-note { margin: 12px 0 0; }
.aa-form { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) auto; gap: 12px; align-items: end; }
.aa-submit { grid-column: auto; padding: 0 16px; white-space: nowrap; }
.aa-result { margin-top: 14px; display: grid; gap: 8px; padding: 12px; border-radius: 10px; border: 0.5px solid var(--border-accent); background: var(--accent-ghost); }
.aa-result-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.aa-small { margin: 0; color: var(--text-muted); font-size: 11px; line-height: 1.5; }
.aa-link { display: inline-flex; align-items: center; gap: 5px; margin-top: 10px; padding: 0; border: 0; background: none; color: var(--text-secondary); font-size: 11.5px; cursor: pointer; }
.aa-link:hover { color: var(--accent); }
.aa-reqs { margin: 8px 0 0; padding-left: 18px; display: grid; gap: 6px; color: var(--text-muted); font-size: 11.5px; line-height: 1.5; }
.aa-reqs strong { color: var(--text-secondary); font-weight: 600; }
.aa-tokens { margin-top: 14px; display: grid; gap: 6px; }
.aa-token { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; padding: 7px 10px; border-radius: 8px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); font-size: 11.5px; }
.aa-token-name { color: var(--text-secondary); min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.aa-token-time { color: var(--text-faint); margin-left: auto; }
.aa-revoke { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; border: 0.5px solid var(--border-subtle); background: transparent; color: var(--text-secondary); font-size: 11px; cursor: pointer; }
.aa-revoke:hover { color: var(--sev-high-color); border-color: var(--sev-high-color); }
.aa-revoke-current { margin-top: 10px; }
@media (max-width: 760px) {
  .aa-form { grid-template-columns: minmax(0, 1fr); }
  .aa-submit { width: 100%; }
  .aa-token-time { margin-left: 0; }
}
`;
