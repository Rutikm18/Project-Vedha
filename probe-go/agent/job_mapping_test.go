package agent

import (
	"reflect"
	"strings"
	"testing"

	"probe-go/pipeline"
)

func TestAdvertisedCapabilitiesHaveExecutablePlans(t *testing.T) {
	for _, capability := range Capabilities {
		if err := pipeline.ValidatePlan(capability, "it"); err != nil {
			t.Fatalf("advertised capability %q is not executable: %v", capability, err)
		}
	}
	for _, unsupported := range []string{
		"mcp_discovery", "passive_discovery", "smb_enum", "snmp_scan", "vuln_scan",
	} {
		if containsString(Capabilities, unsupported) {
			t.Fatalf("unsupported capability %q is still advertised", unsupported)
		}
	}
	if !containsString(Capabilities, "web_tls_scan") {
		t.Fatal("web_tls_scan is implemented but not advertised")
	}
}

func TestMapToJobResolvesCanonicalUseCases(t *testing.T) {
	tests := []struct {
		useCaseID string
		scanType  string
		profile   string
		supported bool
	}{
		{"uc_discovery_only", "discovery", "it", true},
		{"uc_full_assessment", "assessment", "it", true},
		{"uc_external_web_triage", "web_tls_scan", "it", true},
		{"uc_db_exposure", "db_fingerprint", "it", true},
		{"uc_windows_estate", "smb_enum", "it", false},
		{"uc_ot_passive", "passive_discovery", "ot", true},
		{"uc_ai_endpoint_sweep", "mcp_discovery", "it", false},
		{"uc_rescan_delta", "assessment", "it", true},
		{"uc_iot_device_survey", "service_fingerprint", "iot", true},
		{"uc_web_app_triage", "web_scan", "it", true},
		{"uc_udp_service_exposure", "udp_scan", "it", true},
		{"uc_snmp_exposure", "snmp_scan", "it", false},
	}

	for _, tc := range tests {
		t.Run(tc.useCaseID, func(t *testing.T) {
			raw := managerJob(map[string]interface{}{
				"use_case_id": tc.useCaseID,
				"scan_type":   "assessment",
				"profile":     "it",
			})
			job, err := mapToJob(raw)

			if job.ScanType != tc.scanType || job.Profile != tc.profile {
				t.Fatalf(
					"resolved plan = %s/%s, want %s/%s",
					job.ScanType, job.Profile, tc.scanType, tc.profile,
				)
			}
			if tc.supported && err != nil {
				t.Fatalf("supported use case was rejected: %v", err)
			}
			if !tc.supported && (err == nil || !strings.Contains(err.Error(), "unsupported scan_type")) {
				t.Fatalf("unsupported use case error = %v", err)
			}
		})
	}
}

func TestMapToJobUsesParamsScanTypeAndPreservesNarrowTargets(t *testing.T) {
	raw := managerJob(map[string]interface{}{
		"scan_type": "web_tls_scan",
		"profile":   "it",
		"targets":   []interface{}{"10.20.30.7"},
	})

	job, err := mapToJob(raw)
	if err != nil {
		t.Fatalf("map manager job: %v", err)
	}
	if job.ScanType != "web_tls_scan" {
		t.Fatalf("scan type = %q, want web_tls_scan", job.ScanType)
	}
	if !reflect.DeepEqual(job.Targets, []string{"10.20.30.7"}) {
		t.Fatalf("targets = %v, want narrowed target only", job.Targets)
	}
	if !reflect.DeepEqual(job.ScopeCIDRs, []string{"10.20.30.0/24"}) {
		t.Fatalf("authoritative scope = %v", job.ScopeCIDRs)
	}
}

func TestMapToJobMergesAuthoritativeExclusions(t *testing.T) {
	raw := managerJob(map[string]interface{}{
		"scan_type":       "discovery",
		"targets":         []string{"10.20.30.0/29"},
		"_excluded_cidrs": []string{"10.20.30.1/32"},
		"excluded_cidrs":  []string{"10.20.30.2/32", "10.20.30.1/32"},
	})

	job, err := mapToJob(raw)
	if err != nil {
		t.Fatalf("map manager job: %v", err)
	}
	want := []string{"10.20.30.1/32", "10.20.30.2/32"}
	if !reflect.DeepEqual(job.ExcludeCIDRs, want) {
		t.Fatalf("exclusions = %v, want %v", job.ExcludeCIDRs, want)
	}
}

func TestMapToJobFailsClosedOnUnverifiableScope(t *testing.T) {
	tests := []struct {
		name   string
		mutate func(map[string]interface{}, map[string]interface{})
		want   string
	}{
		{
			name: "encrypted_scope",
			mutate: func(raw, params map[string]interface{}) {
				raw["encrypted_scope"] = "ciphertext"
			},
			want: "encrypted scope is unsupported",
		},
		{
			name: "missing_authoritative_scope",
			mutate: func(raw, params map[string]interface{}) {
				delete(params, "_scope_cidrs")
			},
			want: "lacks authoritative _scope_cidrs",
		},
		{
			name: "active_ot_override",
			mutate: func(raw, params map[string]interface{}) {
				params["scan_type"] = "assessment"
				params["profile"] = "ot"
			},
			want: "passive-only",
		},
		{
			name: "unknown_use_case",
			mutate: func(raw, params map[string]interface{}) {
				params["use_case_id"] = "uc_operator_supplied"
			},
			want: "unknown use_case_id",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			raw := managerJob(map[string]interface{}{"scan_type": "discovery"})
			params := raw["params"].(map[string]interface{})
			tc.mutate(raw, params)

			_, err := mapToJob(raw)
			if err == nil || !strings.Contains(err.Error(), tc.want) {
				t.Fatalf("error = %v, want substring %q", err, tc.want)
			}
		})
	}
}

func managerJob(overrides map[string]interface{}) map[string]interface{} {
	params := map[string]interface{}{
		"scan_type":    "discovery",
		"profile":      "it",
		"targets":      []string{"10.20.30.3"},
		"scope_cidrs":  []string{"192.0.2.0/24"},
		"_scope_cidrs": []string{"10.20.30.0/24"},
	}
	for key, value := range overrides {
		params[key] = value
	}
	return map[string]interface{}{
		"job_id":        "11111111-1111-1111-1111-111111111111",
		"engagement_id": "22222222-2222-2222-2222-222222222222",
		"job_type":      "discovery",
		"params":        params,
	}
}
