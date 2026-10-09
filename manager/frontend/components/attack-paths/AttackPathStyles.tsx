import React from "react";
import { OVERVIEW_STYLES } from "./overview-styles";

/** The overview's stylesheet, rendered once by whatever hosts the tiles, rows or card. */
export function AttackPathStyles() {
  return <style>{OVERVIEW_STYLES}</style>;
}
