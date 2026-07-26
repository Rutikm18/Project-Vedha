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
	nets         []*net.IPNet
	hosts        map[string]bool
	excludes     []*net.IPNet
	excludeHosts map[string]bool
}

func NewScopeGuard(entries []string, excludes []string) (*ScopeGuard, error) {
	sg := &ScopeGuard{
		hosts:        make(map[string]bool),
		excludeHosts: make(map[string]bool),
	}
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
			if strings.Contains(e, "/") {
				return nil, fmt.Errorf("invalid scope CIDR %q", e)
			}
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
		} else if strings.Contains(ex, "/") {
			return nil, fmt.Errorf("invalid exclusion CIDR %q", ex)
		} else {
			sg.excludeHosts[strings.ToLower(ex)] = true
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
	if sg.isExcluded(t, ip) {
		return false
	}
	return sg.isAllowed(t, ip)
}

func (sg *ScopeGuard) isAllowed(target string, ip net.IP) bool {
	if sg.hosts[target] {
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

func (sg *ScopeGuard) isExcluded(target string, ip net.IP) bool {
	if sg.excludeHosts[target] {
		return true
	}
	if ip == nil {
		return false
	}
	for _, ex := range sg.excludes {
		if ex.Contains(ip) {
			return true
		}
	}
	return false
}

// ExpandRequested expands only the requested target specifications. The scope
// networks remain an authorization boundary and are never added as targets.
func (sg *ScopeGuard) ExpandRequested(entries []string, maxTargets int) ([]string, error) {
	if maxTargets <= 0 {
		maxTargets = 65536
	}
	out := make([]string, 0)
	seen := make(map[string]bool)

	appendTarget := func(target string) error {
		if seen[target] {
			return nil
		}
		if len(out) >= maxTargets {
			return fmt.Errorf("requested targets exceed safety limit of %d hosts", maxTargets)
		}
		seen[target] = true
		out = append(out, target)
		return nil
	}

	for _, raw := range entries {
		target := strings.TrimSpace(raw)
		if target == "" {
			continue
		}

		if strings.Contains(target, "/") {
			_, requestedNet, err := net.ParseCIDR(target)
			if err != nil {
				return nil, fmt.Errorf("invalid requested CIDR %q", target)
			}
			if !sg.networkAllowed(requestedNet) {
				return nil, fmt.Errorf("requested CIDR %q is outside authorized scope", target)
			}

			ones, bits := requestedNet.Mask.Size()
			if ones < 0 || bits-ones > 16 {
				return nil, fmt.Errorf(
					"requested CIDR %q exceeds safety limit of %d hosts",
					target, maxTargets,
				)
			}
			cur := append(net.IP(nil), requestedNet.IP...)
			for requestedNet.Contains(cur) {
				value := cur.String()
				if sg.InScope(value) {
					if err := appendTarget(value); err != nil {
						return nil, err
					}
				}
				incrementIP(cur)
			}
			continue
		}

		normalized := strings.ToLower(target)
		ip := net.ParseIP(normalized)
		if !sg.isAllowed(normalized, ip) {
			return nil, fmt.Errorf("requested target %q is outside authorized scope", target)
		}
		if sg.isExcluded(normalized, ip) {
			continue
		}
		if ip != nil {
			normalized = ip.String()
		}
		if err := appendTarget(normalized); err != nil {
			return nil, err
		}
	}

	if len(out) == 0 {
		return nil, fmt.Errorf("all requested targets are excluded or empty")
	}
	return out, nil
}

func (sg *ScopeGuard) networkAllowed(requested *net.IPNet) bool {
	last := lastIP(requested)
	for _, allowed := range sg.nets {
		if allowed.Contains(requested.IP) && allowed.Contains(last) {
			return true
		}
	}
	return false
}

func lastIP(network *net.IPNet) net.IP {
	last := append(net.IP(nil), network.IP...)
	for i := range last {
		last[i] |= ^network.Mask[i]
	}
	return last
}

func incrementIP(ip net.IP) {
	for i := len(ip) - 1; i >= 0; i-- {
		ip[i]++
		if ip[i] != 0 {
			return
		}
	}
}
