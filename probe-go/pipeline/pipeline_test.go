package pipeline

import (
	"context"
	"reflect"
	"strings"
	"testing"
)

func TestResolveRequestedHostsDoesNotExpandAuthorizationScope(t *testing.T) {
	job := Job{
		Targets:      []string{"10.20.30.3"},
		ScopeCIDRs:   []string{"10.20.30.0/29"},
		ExcludeCIDRs: []string{"10.20.30.6/32"},
	}

	got, err := resolveRequestedHosts(job)
	if err != nil {
		t.Fatalf("resolve requested hosts: %v", err)
	}
	want := []string{"10.20.30.3"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("resolved hosts = %v, want only requested target %v", got, want)
	}
}

func TestResolveRequestedCIDRAppliesExclusions(t *testing.T) {
	job := Job{
		Targets:      []string{"10.20.30.0/30"},
		ScopeCIDRs:   []string{"10.20.30.0/24"},
		ExcludeCIDRs: []string{"10.20.30.1/32"},
	}

	got, err := resolveRequestedHosts(job)
	if err != nil {
		t.Fatalf("resolve requested CIDR: %v", err)
	}
	want := []string{"10.20.30.0", "10.20.30.2", "10.20.30.3"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("resolved hosts = %v, want %v", got, want)
	}
}

func TestResolveRequestedHostsFailsClosed(t *testing.T) {
	tests := []struct {
		name string
		job  Job
		want string
	}{
		{
			name: "outside_authorized_scope",
			job: Job{
				Targets:    []string{"10.20.31.1"},
				ScopeCIDRs: []string{"10.20.30.0/24"},
			},
			want: "outside authorized scope",
		},
		{
			name: "all_targets_excluded",
			job: Job{
				Targets:      []string{"10.20.30.1"},
				ScopeCIDRs:   []string{"10.20.30.0/24"},
				ExcludeCIDRs: []string{"10.20.30.1/32"},
			},
			want: "all requested targets are excluded",
		},
		{
			name: "oversized_requested_range",
			job: Job{
				Targets:    []string{"10.0.0.0/8"},
				ScopeCIDRs: []string{"10.0.0.0/8"},
			},
			want: "exceeds safety limit",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			hosts, err := resolveRequestedHosts(tc.job)
			if err == nil || !strings.Contains(err.Error(), tc.want) {
				t.Fatalf("error = %v, want substring %q", err, tc.want)
			}
			if len(hosts) != 0 {
				t.Fatalf("fail-closed resolution returned hosts: %v", hosts)
			}
		})
	}
}

func TestOTPlansNeverReachActiveGates(t *testing.T) {
	tests := []struct {
		name     string
		scanType string
		want     string
	}{
		{
			name:     "active_plan_blocked",
			scanType: "assessment",
			want:     "passive-only",
		},
		{
			name:     "passive_collector_unavailable",
			scanType: "passive_discovery",
			want:     "passive collection is unavailable",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := Run(context.Background(), Job{
				ScanType: tc.scanType,
				Profile:  "ot",
				Targets:  []string{"192.0.2.10"},
			}, "test-probe")

			if result.OK {
				t.Fatal("OT plan unexpectedly succeeded")
			}
			if len(result.Facts) != 0 {
				t.Fatalf("OT plan emitted active facts: %v", result.Facts)
			}
			if len(result.Errors) != 1 || !strings.Contains(result.Errors[0], tc.want) {
				t.Fatalf("errors = %v, want substring %q", result.Errors, tc.want)
			}
		})
	}
}

func TestWebTLSPlanEnablesOnlyWebAndTLSBranches(t *testing.T) {
	filter := serviceFilterFor("web_tls_scan")
	if !filter["web"] || !filter["tls"] {
		t.Fatalf("web_tls_scan filter = %v, want web and tls", filter)
	}
	for _, disallowed := range []string{"db", "udp", "nmap"} {
		if filter[disallowed] {
			t.Fatalf("web_tls_scan unexpectedly enables %s", disallowed)
		}
	}
}
