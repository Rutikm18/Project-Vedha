"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "../../hooks/useToast";
import { attackPathsApi } from "../../lib/attack-paths-api";
import { errorMessage } from "../../lib/fetcher";
import type { OverviewRow } from "../../lib/attack-paths";

/** "Compute" for one engagement from a list of them. It is the same explicit action as Recompute on the
 *  engagement's own page (the backend rebuilds and stores that engagement's paths), asked for by a click
 *  on one row: nothing here runs on load, on refetch or for rows nobody clicked. */
export function useComputeAttackPaths() {
  const qc = useQueryClient();
  const toast = useToast();
  const mutation = useMutation({
    mutationFn: (row: OverviewRow) => attackPathsApi.list(row.engagement_id, { refresh: true, pageSize: 1 }),
    onSuccess: (_data, row) => {
      // Every view of the overview, the cards and the engagement's own page now describe an older picture.
      void qc.invalidateQueries({ queryKey: ["console"] , predicate: (q) => q.queryKey[2] === "attackPaths" });
      void qc.invalidateQueries({ queryKey: ["attack-paths-overview"] });
      void qc.invalidateQueries({ queryKey: ["attack-paths-focus"] });
      void qc.invalidateQueries({ queryKey: ["attack-path", row.engagement_id] });
      void qc.invalidateQueries({ queryKey: ["attack-path-analysis", row.engagement_id] });
      toast.success("Attack paths computed", `${row.name}: the row now shows what was found.`);
    },
    onError: (e, row) => toast.error(`Could not compute attack paths for ${row.name}`, errorMessage(e)),
  });
  return {
    run: (row: OverviewRow) => mutation.mutate(row),
    /** The engagement being computed right now, so only its button is busy. */
    pendingId: mutation.isPending ? mutation.variables?.engagement_id ?? null : null,
  };
}
