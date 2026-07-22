// scanner/nmap.go — optional nmap subprocess wrapper.
// When nmap is installed it runs -sT -sV on the already-discovered open ports
// for authoritative service/version labels.  Hidden from console output.
package scanner

import (
	"context"
	"encoding/xml"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

// NmapAvailable returns true if nmap is on PATH.
func NmapAvailable() bool {
	_, err := exec.LookPath("nmap")
	return err == nil
}

type NmapResult struct {
	Host    string
	Port    int
	Proto   string
	State   string
	Service string
	Product string
	Version string
}

// RunNmapVersion runs nmap -sT -sV on host for the given ports and returns
// parsed service/version records.  All nmap output is captured — nothing
// leaks to the console.
func RunNmapVersion(ctx context.Context, host string, ports []int, timeout time.Duration) ([]NmapResult, error) {
	if !NmapAvailable() {
		return nil, fmt.Errorf("nmap not installed")
	}
	if len(ports) == 0 {
		return nil, nil
	}

	portSpec := joinInts(ports, ",")
	args := []string{
		"-sT", "-sV", "--version-intensity", "5",
		"-p", portSpec,
		"-oX", "-",  // output XML to stdout
		"-n",        // no DNS resolution
		"--host-timeout", fmt.Sprintf("%ds", int(timeout.Seconds())),
		host,
	}

	cmdCtx, cancel := context.WithTimeout(ctx, timeout+10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(cmdCtx, "nmap", args...)
	out, err := cmd.Output()
	if err != nil {
		// nmap exits 1 when some hosts are down — treat as partial success
		if len(out) == 0 {
			return nil, fmt.Errorf("nmap failed: %w", err)
		}
	}

	return parseNmapXML(out), nil
}

// nmap XML structs
type nmapRun struct {
	Hosts []nmapHost `xml:"host"`
}
type nmapHost struct {
	Addresses []nmapAddr `xml:"address"`
	Ports     []nmapPort `xml:"ports>port"`
}
type nmapAddr struct {
	Addr     string `xml:"addr,attr"`
	AddrType string `xml:"addrtype,attr"`
}
type nmapPort struct {
	Protocol string    `xml:"protocol,attr"`
	PortID   int       `xml:"portid,attr"`
	State    nmapState `xml:"state"`
	Service  nmapSvc   `xml:"service"`
}
type nmapState struct {
	State string `xml:"state,attr"`
}
type nmapSvc struct {
	Name    string `xml:"name,attr"`
	Product string `xml:"product,attr"`
	Version string `xml:"version,attr"`
}

func parseNmapXML(data []byte) []NmapResult {
	var run nmapRun
	if err := xml.Unmarshal(data, &run); err != nil {
		return nil
	}
	var results []NmapResult
	for _, h := range run.Hosts {
		addr := ""
		for _, a := range h.Addresses {
			if a.AddrType == "ipv4" || addr == "" {
				addr = a.Addr
			}
		}
		for _, p := range h.Ports {
			if p.State.State != "open" {
				continue
			}
			results = append(results, NmapResult{
				Host:    addr,
				Port:    p.PortID,
				Proto:   p.Protocol,
				State:   p.State.State,
				Service: p.Service.Name,
				Product: p.Service.Product,
				Version: p.Service.Version,
			})
		}
	}
	return results
}

func joinInts(ints []int, sep string) string {
	parts := make([]string, len(ints))
	for i, v := range ints {
		parts[i] = fmt.Sprintf("%d", v)
	}
	return strings.Join(parts, sep)
}
