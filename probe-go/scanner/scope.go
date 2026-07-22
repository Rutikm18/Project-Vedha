// scanner/scope.go — authorization allowlist.  Nothing is scanned unless listed.
package scanner

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

type ScopeGuard struct {
	nets     []*net.IPNet
	hosts    map[string]bool
	excludes []*net.IPNet
}

func NewScopeGuard(entries []string, excludes []string) (*ScopeGuard, error) {
	sg := &ScopeGuard{hosts: make(map[string]bool)}
	for _, e := range entries {
		e = strings.TrimSpace(e)
		if e == "" || strings.HasPrefix(e, "#") {
			continue
		}
		// Try CIDR first, then bare IP, then hostname
		if !strings.Contains(e, "/") {
			if ip := net.ParseIP(e); ip != nil {
				bits := 32
				if ip.To4() == nil {
					bits = 128
				}
				e = fmt.Sprintf("%s/%d", e, bits)
			}
		}
		if _, cidr, err := net.ParseCIDR(e); err == nil {
			sg.nets = append(sg.nets, cidr)
		} else {
			sg.hosts[strings.ToLower(e)] = true
		}
	}
	for _, ex := range excludes {
		ex = strings.TrimSpace(ex)
		if ex == "" {
			continue
		}
		if !strings.Contains(ex, "/") {
			if ip := net.ParseIP(ex); ip != nil {
				bits := 32
				if ip.To4() == nil {
					bits = 128
				}
				ex = fmt.Sprintf("%s/%d", ex, bits)
			}
		}
		if _, cidr, err := net.ParseCIDR(ex); err == nil {
			sg.excludes = append(sg.excludes, cidr)
		}
	}
	if len(sg.nets) == 0 && len(sg.hosts) == 0 {
		return nil, fmt.Errorf("scope is empty — no valid CIDRs or hostnames found")
	}
	return sg, nil
}

func ScopeFromFile(path string) (*ScopeGuard, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var entries []string
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if line != "" && !strings.HasPrefix(line, "#") {
			entries = append(entries, line)
		}
	}
	return NewScopeGuard(entries, nil)
}

func (sg *ScopeGuard) InScope(target string) bool {
	t := strings.ToLower(strings.TrimSpace(target))
	ip := net.ParseIP(t)
	// Exclusions win
	if ip != nil {
		for _, ex := range sg.excludes {
			if ex.Contains(ip) {
				return false
			}
		}
	}
	if sg.hosts[t] {
		return true
	}
	if ip == nil {
		return false
	}
	for _, cidr := range sg.nets {
		if cidr.Contains(ip) {
			return true
		}
	}
	return false
}

// ExpandCIDRs returns every IP address that falls within the scope's networks.
// For large CIDRs (>65536 hosts) it returns just the network addresses — the
// caller should use a range sweep instead of enumerating all IPs.
func (sg *ScopeGuard) ExpandCIDRs() []string {
	var out []string
	seen := map[string]bool{}

	for h := range sg.hosts {
		if !seen[h] {
			out = append(out, h)
			seen[h] = true
		}
	}

	for _, cidr := range sg.nets {
		ones, bits := cidr.Mask.Size()
		size := 1 << uint(bits-ones)
		if size > 65536 {
			// Too large to enumerate — return the network address and let the
			// port scanner use a connect-sweep approach with goroutines.
			out = append(out, cidr.String())
			continue
		}
		ip := cidr.IP.To4()
		if ip == nil {
			ip = cidr.IP.To16()
		}
		// Clone so we can increment
		cur := make(net.IP, len(ip))
		copy(cur, ip)
		for cidr.Contains(cur) {
			s := cur.String()
			if !seen[s] {
				out = append(out, s)
				seen[s] = true
			}
			// Increment
			for j := len(cur) - 1; j >= 0; j-- {
				cur[j]++
				if cur[j] != 0 {
					break
				}
			}
		}
	}
	return out
}
