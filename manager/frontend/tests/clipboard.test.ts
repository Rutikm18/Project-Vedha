import assert from "node:assert/strict";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, test } from "node:test";

import { copyText } from "../lib/clipboard";

/* A minimal DOM: enough for the textarea fallback to run and be observed. */
interface FakeArea {
  value: string;
  style: Record<string, string>;
  attrs: Record<string, string>;
  setAttribute(k: string, v: string): void;
  focus(): void;
  select(): void;
  setSelectionRange(a: number, b: number): void;
}

function installDom(opts: {
  secure: boolean;
  clipboard?: { writeText(t: string): Promise<void> };
  execCommand?: (cmd: string) => boolean;
}) {
  const body = { children: [] as FakeArea[], appendChild(n: FakeArea) { this.children.push(n); }, removeChild(n: FakeArea) { this.children = this.children.filter((c) => c !== n); } };
  const executed: { cmd: string; value: string }[] = [];
  const doc = {
    body,
    activeElement: null,
    createElement: (): FakeArea => ({
      value: "", style: {}, attrs: {},
      setAttribute(k, v) { this.attrs[k] = v; },
      focus() {}, select() {}, setSelectionRange() {},
    }),
    execCommand: (cmd: string) => {
      executed.push({ cmd, value: body.children[0]?.value ?? "" });
      return opts.execCommand ? opts.execCommand(cmd) : true;
    },
  };
  Object.assign(globalThis, {
    window: { isSecureContext: opts.secure },
    document: doc,
  });
  Object.defineProperty(globalThis, "navigator", {
    value: { clipboard: opts.clipboard }, configurable: true, writable: true,
  });
  return { body, executed };
}

afterEach(() => {
  for (const k of ["window", "document"]) delete (globalThis as Record<string, unknown>)[k];
});

describe("copyText", () => {
  test("uses the async Clipboard API in a secure context", async () => {
    const written: string[] = [];
    const { executed } = installDom({ secure: true, clipboard: { writeText: async (t) => { written.push(t); } } });
    assert.equal(await copyText("nmap -sV"), true);
    assert.deepEqual(written, ["nmap -sV"]);
    assert.equal(executed.length, 0);
  });

  test("falls back to execCommand on a plain-HTTP origin (no navigator.clipboard)", async () => {
    const { body, executed } = installDom({ secure: false, clipboard: undefined });
    assert.equal(await copyText("sudo systemctl reload nginx"), true);
    assert.deepEqual(executed, [{ cmd: "copy", value: "sudo systemctl reload nginx" }]);
    assert.equal(body.children.length, 0, "the helper textarea is removed");
  });

  test("falls back when the Clipboard API rejects (permission denied)", async () => {
    const { executed } = installDom({
      secure: true,
      clipboard: { writeText: async () => { throw new Error("NotAllowedError"); } },
    });
    assert.equal(await copyText("x"), true);
    assert.equal(executed.length, 1);
  });

  test("reports failure instead of throwing when nothing can copy", async () => {
    installDom({ secure: false, execCommand: () => { throw new Error("unsupported"); } });
    assert.equal(await copyText("x"), false);
  });

  test("no component calls navigator.clipboard directly", () => {
    const root = fileURLToPath(new URL("..", import.meta.url));
    const offenders: string[] = [];
    const walk = (dir: string) => {
      for (const name of readdirSync(dir)) {
        const p = join(dir, name);
        if (statSync(p).isDirectory()) walk(p);
        else if (/\.tsx?$/.test(name) && readFileSync(p, "utf8").includes("navigator.clipboard")) offenders.push(p);
      }
    };
    for (const d of ["app", "components", "lib"]) walk(join(root, d));
    assert.deepEqual(offenders.map((p) => p.slice(root.length)), ["lib/clipboard.ts"]);
  });
});
