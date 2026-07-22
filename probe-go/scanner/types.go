// scanner/types.go — shared result types used by every scanner.
// Schema matches Python probe's ScanResult so the manager accepts both probes.
package scanner

import "time"

type Result struct {
	Scanner   string                 `json:"scanner"`
	Target    string                 `json:"target"`
	Timestamp time.Time              `json:"timestamp"`
	Port      *int                   `json:"port,omitempty"`
	Proto     string                 `json:"proto,omitempty"` // tcp | udp
	Status    string                 `json:"status"`          // open | closed | filtered | error
	Data      map[string]interface{} `json:"data,omitempty"`
	Evidence  string                 `json:"evidence,omitempty"`
	Error     string                 `json:"error,omitempty"`
}

func newResult(scanner, target string) Result {
	return Result{
		Scanner:   scanner,
		Target:    target,
		Timestamp: time.Now().UTC(),
		Data:      make(map[string]interface{}),
	}
}

func ptr(i int) *int { return &i }

// PortResult is the summary produced by Stage 2 (port scan).
type PortResult struct {
	Host    string
	Port    int
	Proto   string // tcp | udp
	Open    bool
	Service string // nmap-style service hint
	Banner  string
}

// HostResult is the output of Stage 1 (host discovery).
type HostResult struct {
	Host  string
	Alive bool
	RTT   time.Duration
}
