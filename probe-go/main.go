// main.go — Vedha Probe (Go) entry point.
//
// USAGE:
//   ./probe                    # run — reads probe.env, registers, starts scanning
//   ./probe --env /path/to.env # use a different env file
//   ./probe --install          # install as launchd/systemd service (needs sudo)
//   ./probe --uninstall        # remove the service
//   ./probe version            # print version
//   ./probe self-test          # connectivity + config check (no scanning)
//
// AUTO-EXECUTE: drop the binary + probe.env on any machine, then:
//   chmod +x probe && sudo ./probe --install
// The probe registers itself with PLATFORM_URL and immediately starts receiving
// scan jobs — no further interaction needed.
package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"

	"probe-go/agent"
	"probe-go/config"
	"probe-go/install"
	"probe-go/pipeline"
)

func main() {
	args := os.Args[1:]

	// Find --env flag
	envFile := envFilePath(args)
	cfg := config.Load(envFile)

	// Sub-commands
	cmd := "run"
	for _, a := range args {
		if a == "--install" {
			cmd = "install"
		} else if a == "--uninstall" {
			cmd = "uninstall"
		} else if a == "version" || a == "--version" || a == "-v" {
			cmd = "version"
		} else if a == "self-test" {
			cmd = "self-test"
		} else if a == "scan" {
			cmd = "scan"
		}
	}

	switch cmd {
	case "version":
		fmt.Printf("Vedha Probe (Go) %s\n", agent.Version)

	case "scan":
		localScan(cfg, args)

	case "install":
		fmt.Println("Installing Vedha Probe as a system service…")
		if err := install.Install("", envFile); err != nil {
			fmt.Fprintf(os.Stderr, "Install failed: %v\n", err)
			os.Exit(1)
		}

	case "uninstall":
		fmt.Println("Removing Vedha Probe service…")
		if err := install.Uninstall(); err != nil {
			fmt.Fprintf(os.Stderr, "Uninstall failed: %v\n", err)
			os.Exit(1)
		}

	case "self-test":
		selfTest(cfg)

	default:
		run(cfg)
	}
}

// localScan runs the full deep pipeline directly against a target — no manager
// required. Usage: ./probe scan <target> [profile]
func localScan(cfg *config.Config, args []string) {
	var target, profile string
	profile = "it"
	for i := 0; i < len(args); i++ {
		a := args[i]
		if a == "scan" {
			if i+1 < len(args) {
				target = args[i+1]
			}
			if i+2 < len(args) && !strings.HasPrefix(args[i+2], "-") {
				profile = args[i+2]
			}
			break
		}
	}
	if target == "" {
		fmt.Println("usage: probe scan <target> [it|iot|ot]")
		fmt.Println("  ./probe scan 127.0.0.1")
		fmt.Println("  ./probe scan 192.168.1.0/24 it")
		os.Exit(2)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() { <-sigs; cancel() }()

	job := pipeline.Job{
		JobID:    "local-scan",
		ScanType: "assessment",
		Profile:  profile,
		Targets:  []string{target},
	}

	fmt.Printf("Vedha Probe — deep scan of %s (profile=%s)\n", target, profile)
	fmt.Println(strings.Repeat("─", 64))

	result := pipeline.Run(ctx, job, cfg.ProbeName)
	renderReport(result)
}

// renderReport prints a clean per-host table + ranked findings.
func renderReport(r pipeline.Result) {
	// Per-host service table
	for _, host := range r.Hosts {
		ip, _ := host["ip"].(string)
		ports, _ := host["ports"].([]map[string]interface{})
		if len(ports) == 0 {
			continue
		}
		fmt.Printf("\nHOST %s\n", ip)
		// Merge fingerprint facts for product/version per port
		for _, p := range ports {
			port := fmt.Sprintf("%v", p["port"])
			proto, _ := p["protocol"].(string)
			svc, _ := p["service"].(string)
			label := findServiceLabel(r.Facts, ip, p["port"])
			fmt.Printf("  %-10s %-14s %s\n", port+"/"+proto, svc, label)
		}
	}

	// Ranked findings
	if len(r.Findings) > 0 {
		fmt.Printf("\nNOTABLE FINDINGS (%d)\n", len(r.Findings))
		for _, f := range r.Findings {
			kev := ""
			if f.KEV {
				kev = " [KNOWN-EXPLOITED]"
			}
			where := f.Host
			if f.Port > 0 {
				where = fmt.Sprintf("%s %s/%d", f.Host, protoOr(f.Proto), f.Port)
			}
			fmt.Printf("  [%-8s] %s — %s%s\n", strings.ToUpper(f.Severity), where, f.Title, kev)
			if f.Evidence != "" {
				fmt.Printf("             evidence: %s\n", f.Evidence)
			}
		}
	}

	fmt.Println(strings.Repeat("─", 64))
	fmt.Printf("[summary] %d host(s), %d open port(s), %d fact(s), %d finding(s)\n",
		r.HostCount, r.OpenPorts, r.FactCount, r.FindingCount)
	if len(r.Errors) > 0 {
		fmt.Printf("[errors] %v\n", r.Errors)
	}
}

// findServiceLabel pulls the best product/version string for a host:port from facts.
func findServiceLabel(facts []pipeline.Fact, host string, port interface{}) string {
	best := ""
	for _, f := range facts {
		if f["target"] != host {
			continue
		}
		if fmt.Sprintf("%v", f["port"]) != fmt.Sprintf("%v", port) {
			continue
		}
		data, _ := f["data"].(map[string]interface{})
		if data == nil {
			continue
		}
		product, _ := data["product"].(string)
		version, _ := data["version"].(string)
		title, _ := data["title"].(string)
		server, _ := data["server"].(string)
		parts := []string{}
		for _, s := range []string{product, version} {
			if s != "" {
				parts = append(parts, s)
			}
		}
		if server != "" {
			parts = append(parts, "server="+server)
		}
		if title != "" {
			parts = append(parts, fmt.Sprintf("title=%q", title))
		}
		if cand := strings.Join(parts, " "); len(cand) > len(best) {
			best = cand
		}
	}
	return best
}

func protoOr(p string) string {
	if p == "" {
		return "tcp"
	}
	return p
}

// run starts the agent and blocks until SIGINT/SIGTERM.
func run(cfg *config.Config) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Graceful shutdown on SIGINT or SIGTERM
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigs
		fmt.Println("\nShutting down…")
		cancel()
	}()

	a := agent.New(cfg)
	if err := a.Run(ctx); err != nil {
		fmt.Fprintf(os.Stderr, "Probe error: %v\n", err)
		os.Exit(1)
	}
}

func selfTest(cfg *config.Config) {
	fmt.Println("Self-test…")
	ok := true

	check := func(name string, pass bool, detail string) {
		if pass {
			fmt.Printf("  ✓ %-20s %s\n", name, detail)
		} else {
			fmt.Printf("  ✗ %-20s %s\n", name, detail)
			ok = false
		}
	}

	check("PLATFORM_URL", cfg.PlatformURL != "", cfg.PlatformURL)
	check("OPERATOR_EMAIL", cfg.OperatorEmail != "", cfg.OperatorEmail)
	check("OPERATOR_PASSWORD", cfg.OperatorPassword != "", "(set)")
	check("PROBE_NAME", cfg.ProbeName != "", cfg.ProbeName)
	check("SPOOL_DIR writable", isDirWritable(cfg.SpoolDir), cfg.SpoolDir)

	if ok {
		fmt.Println("Self-test PASSED")
	} else {
		fmt.Println("Self-test FAILED — fix the issues above, then rerun.")
		os.Exit(1)
	}
}

func envFilePath(args []string) string {
	// Check --env <path> flag
	for i, a := range args {
		if a == "--env" && i+1 < len(args) {
			return args[i+1]
		}
	}
	// Check PROBE_ENV_FILE env var (set by the service installer)
	if v := os.Getenv("PROBE_ENV_FILE"); v != "" {
		return v
	}
	// Default: probe.env next to the binary
	exe, _ := os.Executable()
	return filepath.Join(filepath.Dir(exe), "probe.env")
}

func isDirWritable(dir string) bool {
	if err := os.MkdirAll(dir, 0700); err != nil {
		return false
	}
	tmp := filepath.Join(dir, ".write-test")
	if err := os.WriteFile(tmp, []byte("ok"), 0600); err != nil {
		return false
	}
	os.Remove(tmp)
	return true
}
