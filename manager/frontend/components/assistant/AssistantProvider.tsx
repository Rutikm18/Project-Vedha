"use client";
import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { usePathname } from "next/navigation";
import { AssistantFab } from "./AssistantFab";
import { AssistantDrawer } from "./AssistantDrawer";
import {
  canMountAssistant,
  isAssistantRoute,
  type AssistantAuthState,
} from "../../lib/assistant-access";

type Ctx = {
  open: boolean;
  findingId: string | null;
  findingIds: string[];
  explain: (id: string) => void;
  explainMany: (ids: string[]) => void;
  openBlank: () => void;
  close: () => void;
};

const AssistantCtx = createContext<Ctx | null>(null);

export function useAssistant(): Ctx {
  const c = useContext(AssistantCtx);
  if (!c) throw new Error("useAssistant must be used within AssistantProvider");
  return c;
}

export function AssistantProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const routeEnabled = isAssistantRoute(pathname);
  const [authCheck, setAuthCheck] = useState<{
    pathname: string | null;
    state: AssistantAuthState;
  }>({ pathname: null, state: "checking" });
  const authState = authCheck.pathname === pathname ? authCheck.state : "checking";
  const assistantEnabled = canMountAssistant(pathname, authState);
  const [openPathname, setOpenPathname] = useState<string | null>(null);
  const open = assistantEnabled && openPathname === pathname;
  const [findingId, setFindingId] = useState<string | null>(null);
  const [findingIds, setFindingIds] = useState<string[]>([]);

  useEffect(() => {
    if (!routeEnabled) return;

    const controller = new AbortController();
    fetch("/api/auth/me", {
      cache: "no-store",
      credentials: "same-origin",
      signal: controller.signal,
    })
      .then((response) => {
        if (!controller.signal.aborted) {
          setAuthCheck({
            pathname,
            state: response.ok ? "authenticated" : "anonymous",
          });
        }
      })
      .catch((error: unknown) => {
        if (!controller.signal.aborted && !(error instanceof DOMException && error.name === "AbortError")) {
          setAuthCheck({ pathname, state: "anonymous" });
        }
      });

    return () => controller.abort();
  }, [pathname, routeEnabled]);

  const explain = useCallback((id: string) => {
    setFindingId(id);
    setFindingIds([id]);
    setOpenPathname(pathname);
  }, [pathname]);
  const explainMany = useCallback((ids: string[]) => {
    const selected = [...new Set(ids)].slice(0, 20);
    setFindingIds(selected);
    setFindingId(selected.length === 1 ? selected[0] : null);
    setOpenPathname(pathname);
  }, [pathname]);
  const openBlank = useCallback(() => {
    setFindingId(null);
    setFindingIds([]);
    setOpenPathname(pathname);
  }, [pathname]);
  const close = useCallback(() => setOpenPathname(null), []);

  useEffect(() => {
    if (!assistantEnabled) return;
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setFindingId(null);
        setFindingIds([]);
        setOpenPathname((current) => current === pathname ? null : pathname);
      }
      if (e.key === "Escape") setOpenPathname(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [assistantEnabled, pathname]);

  return (
    <AssistantCtx.Provider value={{ open, findingId, findingIds, explain, explainMany, openBlank, close }}>
      {children}
      {assistantEnabled && <AssistantFab />}
      {assistantEnabled && <AssistantDrawer key={findingIds.join(":") || "blank"} />}
    </AssistantCtx.Provider>
  );
}
