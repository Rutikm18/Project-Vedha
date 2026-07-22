// scanner/port.go — Gate 2: TCP port scanner (pure Go, no nmap required).
// Uses a bounded goroutine pool so concurrency stays deterministic.
package scanner

import (
	"context"
	"fmt"
	"net"
	"sync"
	"time"
)

// Profile port lists — verbatim from gates.py / pipeline.py.
var ProfilePorts = map[string][]int{
	"it": {
		21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 389, 443, 445, 465, 587,
		636, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 5985, 5986, 6379,
		8000, 8080, 8443, 9200, 11211, 27017,
	},
	"iot": {
		22, 23, 80, 443, 554, 1883, 8883, 5683, 8080, 8443, 8888, 9000, 9100,
		49152, 62078, 5000, 8081, 37777,
	},
	"ot": {
		102, 502, 503, 20000, 44818, 47808, 2404, 4840,
	},
}

// ScanPorts runs a TCP connect sweep against host:ports with bounded
// concurrency and per-dial timeout.  Returns only open ports.
func ScanPorts(ctx context.Context, host string, ports []int, concurrency int, timeout time.Duration) []PortResult {
	if concurrency <= 0 {
		concurrency = 200
	}
	sem := make(chan struct{}, concurrency)
	var mu sync.Mutex
	var open []PortResult
	var wg sync.WaitGroup

	for _, p := range ports {
		p := p
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

			addr := fmt.Sprintf("%s:%d", host, p)
			dialer := &net.Dialer{}
			dctx, cancel := context.WithTimeout(ctx, timeout)
			defer cancel()

			conn, err := dialer.DialContext(dctx, "tcp", addr)
			if err == nil {
				conn.Close()
				mu.Lock()
				open = append(open, PortResult{Host: host, Port: p, Proto: "tcp", Open: true})
				mu.Unlock()
			}
		}()
	}
	wg.Wait()
	return open
}

// PortRange expands a start-end range into a port list.
func PortRange(start, end int) []int {
	if start < 1 {
		start = 1
	}
	if end > 65535 {
		end = 65535
	}
	ports := make([]int, 0, end-start+1)
	for i := start; i <= end; i++ {
		ports = append(ports, i)
	}
	return ports
}
