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
  AgentInstallInfo, FleetEngagementOption, FleetWorkspaceSurface, InstallCommands, InstallToken,
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

/** One sentence with exactly one closing full stop, whatever the server sent. */
export function sentence(text: string | null | undefined): string {
  const t = (text ?? "").trim().replace(/[.\s]+$/, "");
  return t ? `${t}.` : "";
}

export type InstallOs = "linux" | "windows";

/** Whether the published release can be installed on Windows (and the manager says so). */
export function windowsOffered(info: AgentInstallInfo | null): boolean {
  return Boolean(info?.available && info.windows?.available);
}

/** The Windows one-liners worth showing, in the order to prefer them. */
export function windowsCommands(commands: InstallCommands | undefined): { key: string; label: string; command: string }[] {
  const out: { key: string; label: string; command: string }[] = [];
  if (commands?.windows_powershell) {
    out.push({ key: "powershell", label: "Paste into any Command Prompt or PowerShell window — Windows asks for administrator permission itself", command: commands.windows_powershell });
  }
  if (commands?.windows_cmd) {
    out.push({ key: "cmd", label: "Alternative for Command Prompt (also asks for administrator rights itself)", command: commands.windows_cmd });
  }
  return out;
}

/** The Windows commands for an install with NO token (approval install), or [] while the manager does not allow it. */
export function tokenlessWindowsCommands(info: AgentInstallInfo | null): { key: string; label: string; command: string }[] {
  if (!info?.available || !info.tokenless?.enabled || !windowsOffered(info)) return [];
  return windowsCommands(info.tokenless.commands as InstallCommands);
}

/** What an operator should do when no release is published yet. Windows first, because that is the common case. */
export function publishAdvice(): { windows: string; linux: string } {
  return {
    windows: "powershell -ExecutionPolicy Bypass -File probe\\windows\\publish-release.ps1 -Server user@your-server -ManagerUrl https://api.your-domain -ConfigureManager",
    linux: "make agent-release   then   make agent-publish TO=user@your-server:/opt/Project-Vedha/manager/agent-releases",
  };
}

/** One honest sentence on what protects the Windows download. */
export function windowsIntegrity(info: AgentInstallInfo | null): string {
  const windows = info?.windows;
  if (!windows?.available) return "";
  return windows.authenticode_thumbprint
    ? `vedha-agent.exe is Authenticode-signed (certificate ${windows.authenticode_thumbprint.slice(0, 8)}…) and the installer checks it`
    : "not Authenticode-signed yet — the installer still verifies the signed release manifest and the package checksum";
}

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
  // Windows is the common client host, so it leads: the OS defaults to Windows and
  // falls back to Linux only when the release has no Windows package.
  const [os, setOs] = useState<InstallOs>("windows");

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
  const hasWindows = windowsOffered(info);
  const target: InstallOs = hasWindows ? os : "linux";
  const winCommands = windowsCommands(created?.commands);
  const noTokenCommands = tokenlessWindowsCommands(info);
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
            Runs on a Linux host with Docker{hasWindows ? " or on a Windows host" : ""} inside the network you want assessed. It only connects
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
                {" "}{sentence(info.reason)} Nothing can be installed until one signed release is published. One command does the
                whole job (build, sign, upload, set the keys on the manager, restart it):
                <div className="flt-install" style={{ marginTop: 6 }}>
                  <code className="flt-code">{publishAdvice().windows}</code>
                  <button className="flt-icon-btn" aria-label="Copy the publish command" onClick={() => copy(publishAdvice().windows)}>
                    <Clipboard size={15} />
                  </button>
                </div>
                <span className="aa-small">
                  Run it on your Windows PC (steps and what it does: docs/operations/ONE_COMMAND_INSTALL.md). On Linux or macOS use{" "}
                  <span className="flt-mono">{publishAdvice().linux}</span>, then set{" "}
                  <span className="flt-mono">AGENT_RELEASE_PUBLIC_KEY</span> (and, for Windows,{" "}
                  <span className="flt-mono">AGENT_RELEASE_P256_PUBLIC_KEY</span>) on the manager.
                </span>
              </>
            ) : " Your Vedha team needs to publish it — contact them, then come back to this page."}
          </div>
        </div>
      ) : (
        <div className="aa-release" aria-label="Agent release">
          <CheckCircle2 size={13} color="var(--nominal-color)" />
          <span>Agent <strong className="flt-mono">{info.version}</strong></span>
          <span className="aa-dot">·</span>
          <span>{[...(info.arches ?? []).map((a) => `linux/${a}`), ...(hasWindows ? ["windows/amd64"] : [])].join(", ")}</span>
          <span className="aa-dot">·</span>
          <span>{info.signed ? <>signed <span className="flt-mono">({info.signing_key_id})</span></> : "unsigned (development)"}</span>
        </div>
      )}

      {surface === "manager" && info && !info.manager_url_configured && (
        <p className="flt-warn">MANAGER_PUBLIC_URL is not set on the API, so commands use {info.manager_url || "this request's address"}. Set it to the public API URL (for example https://api.your-domain.com).</p>
      )}
      {blocked && info?.blocker && (
        <div className="aa-note" role="status"><AlertTriangle size={14} /><div>{sentence(info.blocker)}</div></div>
      )}

      {noTokenCommands.length > 0 && (
        <div className="aa-result" aria-label="Install without a token">
          <div className="aa-result-head">
            <span className="flt-cmd-label">Windows — no token needed (approve it here afterwards)</span>
          </div>
          <div className="flt-cmds">
            {noTokenCommands.map((c) => (
              <div className="flt-cmd" key={c.key}>
                <span className="flt-cmd-label">{c.label}</span>
                <div className="flt-install">
                  <code className="flt-code">{c.command}</code>
                  <button className="flt-icon-btn" aria-label={`Copy ${c.key} command without a token`} onClick={() => copy(c.command)}>
                    <Clipboard size={15} />
                  </button>
                </div>
              </div>
            ))}
          </div>
          <p className="aa-small">
            The command holds no secret, so it can be reused on any number of machines. Each machine installs, connects to
            this manager and shows a short <strong>pairing code</strong>. Find it under <strong>Pending requests</strong> below
            (check the host name and IP address), type the code, and approve: the manager then gives that agent its
            credentials by itself. Nothing is scanned until you approve, and the request expires after 15 minutes.
          </p>
        </div>
      )}

      <form className="aa-form" onSubmit={generate}>
        {surface === "manager" && (
          <label className="flt-field aa-field-full">
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
          {hasWindows && (
            <div className="aa-os" role="tablist" aria-label="Operating system of the host">
              {(["windows", "linux"] as const).map((id) => (
                <button
                  key={id}
                  type="button"
                  role="tab"
                  aria-selected={target === id}
                  className="aa-os-tab"
                  data-active={target === id}
                  onClick={() => setOs(id)}
                >
                  {id === "linux" ? "Linux" : "Windows"}
                </button>
              ))}
            </div>
          )}
          <div className="aa-result-head">
            <span className="flt-cmd-label">
              {target === "windows" ? "Run on the Windows host (one command, any window)" : "Run on the Linux host (as root)"}
            </span>
            <span className="flt-state" style={{ color: STATE_COLOR[createdState ?? "active"] }}>
              <span className="flt-dot" style={{ background: STATE_COLOR[createdState ?? "active"] }} />
              {STATE_LABEL[createdState ?? "active"]}
            </span>
          </div>
          {target === "windows" ? (
            <div className="flt-cmds">
              {winCommands.length === 0 && (
                <p className="aa-small">This manager address cannot be embedded safely in a Windows command. Use the https:// address of the manager.</p>
              )}
              {winCommands.map((c) => (
                <div className="flt-cmd" key={c.key}>
                  <span className="flt-cmd-label">{c.label}</span>
                  <div className="flt-install">
                    <code className="flt-code">{c.command}</code>
                    <button className="flt-icon-btn" aria-label={`Copy ${c.key} install command`} onClick={() => copy(c.command)}>
                      <Clipboard size={15} />
                    </button>
                  </div>
                </div>
              ))}
              <p className="aa-small">{windowsIntegrity(info)}.</p>
            </div>
          ) : (
            <div className="flt-install">
              <code className="flt-code">{created.commands.one_line}</code>
              <button className="flt-icon-btn" aria-label="Copy install command" onClick={() => copy(created.commands!.one_line)}>
                <Clipboard size={15} />
              </button>
            </div>
          )}
          <p className="aa-small">
            Works once, until {formatExact(created.expires_at)}. Anyone holding it can add an agent to
            this engagement until then — share it only with the person installing, or revoke it below.
            {createdState === "used" && " The agent has enrolled; it appears under Connected vedha-agents."}
          </p>
          <button type="button" className="aa-link" onClick={() => setShowInspect((v) => !v)} aria-expanded={showInspect}>
            <ChevronDown size={12} className="flt-chev" data-open={showInspect} /> Prefer to read the installer first?
          </button>
          {showInspect && target === "windows" && (
            <p className="aa-small">
              The installer is plain text: open <a className="flt-mono" href={`${info?.manager_url ?? ""}/agent/install.ps1`} target="_blank" rel="noreferrer">{host}/agent/install.ps1</a> and
              read it before running the command. It verifies the signed release before it installs anything
              (add <span className="flt-mono">-VerifyOnly</span> to check a release without installing it).
            </p>
          )}
          {showInspect && target === "linux" && (
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
      {showReqs && target === "windows" && (
        <ul className="aa-reqs">
          <li><strong>Host:</strong> 64-bit Windows 10 / 11 or Windows Server 2016+, Windows PowerShell 5.1 or later, an account that can approve the administrator prompt (UAC). The manager must be reachable over https.</li>
          <li><strong>Placement:</strong> on the same network segment as the systems in scope, with a fixed IP (DHCP reservation).</li>
          <li><strong>Network:</strong> outbound HTTPS (443) to <span className="flt-mono">{host}</span>; working time sync. No inbound ports.</li>
          <li><strong>Security tools:</strong> a network scanner can look like malware to antivirus/EDR. Allow-list <span className="flt-mono">vedha-agent.exe</span> with your security team before installing.</li>
          <li><strong>Where it lives:</strong> a background task named VedhaAgent running as SYSTEM; its identity key is in <span className="flt-mono">C:\ProgramData\vedha-agent</span>, readable by administrators only. Remove it with <span className="flt-mono">C:\ProgramData\vedha-agent\tools\uninstall.cmd -Purge</span>.</li>
          <li><strong>Integrity:</strong> the installer verifies the signed release manifest, the package checksum and (when the release pins one) the Authenticode signature before installing.</li>
        </ul>
      )}
      {showReqs && target === "linux" && (
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
/* A long command must scroll inside its own box, never widen the card. Every flex/grid
   ancestor between the scrolling .flt-code and the card must be allowed to shrink — including
   the zero-knowledge (.aa-zk) block, whose long Windows one-liner escapes the card otherwise. */
.flt-card, .aa-note > div,
.aa-result, .aa-result > *, .aa-result .flt-cmds, .aa-result .flt-cmd,
.aa-zk, .aa-zk > *,
.flt-cmds, .flt-cmd, .flt-install { min-width: 0; }
.flt-code { scrollbar-width: thin; }
.aa-warn { border-color: var(--sev-medium-color); }
.aa-form + .aa-note { margin: 12px 0 0; }
/* Engagement (what the agent scans for — required, scope-defining) leads full-width; Label
   (optional id) and Command-lifetime (the generated command's security window) pair on one row;
   the action spans the foot. No field is ever orphaned into a narrow column. */
.aa-form { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 14px; align-items: start; }
.aa-field-full { grid-column: 1 / -1; }
.aa-submit { grid-column: 1 / -1; padding: 0 16px; white-space: nowrap; }
.aa-result { margin-top: 14px; display: grid; gap: 8px; padding: 12px; border-radius: 10px; border: 0.5px solid var(--border-accent); background: var(--accent-ghost); }
.aa-result-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.aa-small { margin: 0; color: var(--text-muted); font-size: 11px; line-height: 1.5; }
.aa-os { display: inline-flex; gap: 2px; padding: 2px; border-radius: 8px; border: 0.5px solid var(--border-subtle); background: var(--bg-surface); width: fit-content; }
.aa-os-tab { padding: 4px 14px; border: 0; border-radius: 6px; background: transparent; color: var(--text-secondary); font-size: 11.5px; cursor: pointer; }
.aa-os-tab[data-active="true"] { background: var(--accent-ghost); color: var(--accent); font-weight: 600; }
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
