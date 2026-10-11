"use client";
import React, { useState } from "react";
import {
  AlertTriangle, Building2, Check, CheckCircle2, Copy, ShieldCheck,
  Sparkles, Terminal, Wrench,
} from "lucide-react";
import type { AdvisorVM } from "../../lib/assistant";
import { copyText } from "../../lib/clipboard";
import { InlineText } from "./AssistantText";

/** Inline Markdown (bold, italic, code, links) in advisor sentences. */
const RichText = ({ text }: { text: string }) => <InlineText text={text} />;

function CopyButton({ value }: { value: string }) {
  const [state, setState] = useState<"idle" | "copied" | "failed">("idle");
  const label = state === "copied" ? "Copied" : state === "failed" ? "Copy failed — select and copy manually" : "Copy command";
  return (
    <button
      type="button"
      className="advisor-copy"
      aria-label={label}
      title={label}
      onClick={() => {
        void copyText(value).then((ok) => {
          setState(ok ? "copied" : "failed");
          window.setTimeout(() => setState("idle"), 1600);
        });
      }}
    >
      {state === "copied" ? <Check size={13} /> : state === "failed" ? <AlertTriangle size={13} /> : <Copy size={13} />}
    </button>
  );
}

function CommandRow({ command }: { command: string }) {
  return (
    <div className="advisor-cmd">
      <code>{command}</code>
      <CopyButton value={command} />
    </div>
  );
}

function Section({ icon, title, children }: { icon: React.ReactNode; title: string; children: React.ReactNode }) {
  return (
    <div className="advisor-section">
      <span className="advisor-section-icon">{icon}</span>
      <div className="advisor-section-body">
        <h4>{title}</h4>
        {children}
      </div>
    </div>
  );
}

const PATCH_PILL: Record<AdvisorVM["patch"]["available"], { label: string; color: string; bg: string }> = {
  yes:     { label: "PATCH AVAILABLE", color: "var(--nominal-color)",       bg: "var(--nominal-bg)" },
  no:      { label: "NO PATCH",        color: "var(--sev-critical-color)",  bg: "var(--sev-critical-bg)" },
  unknown: { label: "PATCH UNKNOWN",   color: "var(--text-muted)",          bg: "var(--bg-surface)" },
};

export function AdvisorFlow({ vm }: { vm: AdvisorVM }) {
  const pill = PATCH_PILL[vm.patch.available];
  return (
    <div className="advisor-flow">
      {/* 1 — What it is */}
      <Section icon={<ShieldCheck size={15} />} title="What is the vulnerability?">
        <p><RichText text={vm.whatIs} /></p>
      </Section>

      {/* 2 — Impact */}
      {vm.impact.length > 0 && (
        <Section icon={<Building2 size={15} />} title="What is the impact?">
          <ul className="advisor-list">
            {vm.impact.map((point, i) => <li key={i}><RichText text={point} /></li>)}
          </ul>
        </Section>
      )}

      {/* 3 — Verify */}
      <Section icon={<Terminal size={15} />} title="How to verify">
        {vm.verify.command
          ? <CommandRow command={vm.verify.command} />
          : <p><RichText text={vm.verify.statement} /></p>}
        {vm.verify.command && vm.verify.statement && (
          <p className="advisor-subnote">{vm.verify.statement}</p>
        )}
        {vm.verify.caveat && (
          <div className="advisor-caveat">
            <AlertTriangle size={12} />
            <span>{vm.verify.caveat}</span>
          </div>
        )}
      </Section>

      {/* 4 — Patch available */}
      <Section icon={<CheckCircle2 size={15} />} title="Is a patch available?">
        <div className="advisor-patch-row">
          <span className="advisor-patch-pill" style={{ color: pill.color, background: pill.bg, borderColor: pill.color }}>
            {vm.patch.available === "yes" ? <Check size={11} /> : vm.patch.available === "no" ? <AlertTriangle size={11} /> : null}
            {pill.label}
          </span>
          {vm.patch.summary && <span className="advisor-patch-summary"><RichText text={vm.patch.summary} /></span>}
        </div>
      </Section>

      {/* 5 — How to patch */}
      <Section icon={<Wrench size={15} />} title="How to patch">
        {vm.patchSteps.length ? (
          <ol className="advisor-steps">
            {vm.patchSteps.map((step, i) => (
              <li key={i}>
                <div className="advisor-step-head">
                  <p><RichText text={step.description} /></p>
                  <span className={`advisor-ground ${step.grounded ? "is-grounded" : "is-adapt"}`}>
                    {step.grounded
                      ? <><CheckCircle2 size={10} /> vendor-documented</>
                      : <><AlertTriangle size={10} /> adapt to your environment</>}
                  </span>
                </div>
                {step.command && <CommandRow command={step.command} />}
              </li>
            ))}
          </ol>
        ) : (
          <p className="advisor-empty">No patch steps available — see the references on the brief above.</p>
        )}
      </Section>

      {/* 6 — Further hardening */}
      {vm.improvements.length > 0 && (
        <Section icon={<Sparkles size={15} />} title="Further hardening">
          <ul className="advisor-list">
            {vm.improvements.map((point, i) => <li key={i}><RichText text={point} /></li>)}
          </ul>
        </Section>
      )}
    </div>
  );
}
