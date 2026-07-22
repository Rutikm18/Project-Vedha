// scanner/discover.go — Gate 1: host discovery.
// Probes each IP with a TCP SYN to port 80 and 443 (no ICMP needed, no root).
// Falls back to trying ports 22, 8080 if both fail.
package scanner

import (
	"context"
	"net"
	"sync"
	"time"
)

var discoveryProbes = []int{80, 443, 22, 8080, 8443}

// DiscoverHosts checks which hosts in the list respond to a TCP probe.
// concurrency bounds simultaneous dials.
func DiscoverHosts(ctx context.Context, hosts []string, concurrency int, timeout time.Duration) []HostResult {
	if concurrency <= 0 {
		concurrency = 200
	}
	sem := make(chan struct{}, concurrency)
	var mu sync.Mutex
	var results []HostResult
	var wg sync.WaitGroup

	for _, h := range hosts {
		h := h
		wg.Add(1)
		go func() {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()

			select {
			case <-ctx.Done():
				return
			default:
			}

			alive, rtt := probeAlive(h, timeout)
			mu.Lock()
			results = append(results, HostResult{Host: h, Alive: alive, RTT: rtt})
			mu.Unlock()
		}()
	}
	wg.Wait()
	return results
}

func probeAlive(host string, timeout time.Duration) (bool, time.Duration) {
	for _, port := range discoveryProbes {
		start := time.Now()
		addr := net.JoinHostPort(host, intStr(port))
		conn, err := net.DialTimeout("tcp", addr, timeout)
		if err == nil {
			conn.Close()
			return true, time.Since(start)
		}
		// A refused connection (RST) means the host is alive even though the
		// port is closed — distinguish from timeout/no-route.
		if isRefused(err) {
			return true, time.Since(start)
		}
	}
	return false, 0
}

func isRefused(err error) bool {
	if ne, ok := err.(*net.OpError); ok {
		if se, ok := ne.Err.(*net.OpError); ok {
			_ = se
		}
		return ne.Op == "dial" && ne.Err != nil &&
			(containsStr(ne.Err.Error(), "refused") || containsStr(ne.Err.Error(), "connection refused"))
	}
	return containsStr(err.Error(), "connection refused")
}

func containsStr(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || len(s) > 0 && findStr(s, sub))
}

func findStr(s, sub string) bool {
	for i := 0; i <= len(s)-len(sub); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

func intStr(i int) string {
	const digits = "0123456789"
	if i == 0 {
		return "0"
	}
	b := make([]byte, 0, 6)
	for i > 0 {
		b = append([]byte{digits[i%10]}, b...)
		i /= 10
	}
	return string(b)
}
