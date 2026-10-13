import type { FindingAssessment } from "./attack-assessments";

export const environmentBase = "/api/attack-paths/environment-assessments";
export interface EnvironmentOptions { items: {id:string;name:string}[]; truncated:boolean; can_compute:boolean; }
export interface EnvironmentSnapshot { id:string;status:"queued"|"running"|"completed"|"failed";engagement_ids:string[];effective_as_of:string;failure_code:string|null;requires_reassessment:boolean; }
export interface EnvironmentHistory { latest_request:EnvironmentSnapshot|null;last_completed:EnvironmentSnapshot|null; }
export interface EnvironmentFinding extends FindingAssessment { engagement_id:string;engagement_name:string;asset_id:string|null; }
export interface EnvironmentResult { snapshot:EnvironmentSnapshot;items:EnvironmentFinding[];total:number;total_findings:number;page:number;page_size:number;compute:string;coverage:string;sources:{engagement_id:string;engagement_name:string;snapshot_id:string}[];systems:{id:string;asset_id:string;engagement_id:string;label:string}[];engine:{supported_proofs:unknown[];realization:string};bridge_state:string;missing_relationships:string[]; }
