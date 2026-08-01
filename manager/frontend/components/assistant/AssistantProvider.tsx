"use client";
import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { AssistantFab } from "./AssistantFab";
import { AssistantDrawer } from "./AssistantDrawer";

type Ctx = {
  open: boolean;
  findingId: string | null;
  explain: (id: string) => void;
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
  const [open, setOpen] = useState(false);
  const [findingId, setFindingId] = useState<string | null>(null);

  const explain = useCallback((id: string) => {
    setFindingId(id);
    setOpen(true);
  }, []);
  const openBlank = useCallback(() => {
    setFindingId(null);
    setOpen(true);
  }, []);
  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      }
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <AssistantCtx.Provider value={{ open, findingId, explain, openBlank, close }}>
      {children}
      <AssistantFab />
      <AssistantDrawer key={findingId ?? "blank"} />
    </AssistantCtx.Provider>
  );
}
