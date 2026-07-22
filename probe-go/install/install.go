// install/install.go — self-install as launchd (macOS) or systemd (Linux) service.
// Run `probe --install` once; the binary auto-starts on every boot.
package install

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

const (
	launchdPlist   = "/Library/LaunchDaemons/com.vedha.probe.plist"
	systemdService = "/etc/systemd/system/vedha-probe.service"
)

// Install copies the current binary to /usr/local/bin and creates a service.
func Install(binaryPath, envFile string) error {
	if binaryPath == "" {
		var err error
		binaryPath, err = os.Executable()
		if err != nil {
			return fmt.Errorf("cannot determine binary path: %w", err)
		}
	}
	binaryPath, _ = filepath.Abs(binaryPath)
	envFile, _ = filepath.Abs(envFile)

	// Copy binary to a stable location
	dest := "/usr/local/bin/vedha-probe"
	if err := copyFile(binaryPath, dest); err != nil {
		return fmt.Errorf("cannot copy binary to %s: %w (try sudo)", dest, err)
	}
	os.Chmod(dest, 0755)

	switch runtime.GOOS {
	case "darwin":
		return installLaunchd(dest, envFile)
	case "linux":
		return installSystemd(dest, envFile)
	default:
		return fmt.Errorf("auto-install not supported on %s — run manually: %s", runtime.GOOS, dest)
	}
}

// Uninstall stops and removes the service.
func Uninstall() error {
	switch runtime.GOOS {
	case "darwin":
		exec.Command("launchctl", "unload", launchdPlist).Run()
		os.Remove(launchdPlist)
		os.Remove("/usr/local/bin/vedha-probe")
		fmt.Println("Probe service removed (macOS)")
	case "linux":
		exec.Command("systemctl", "stop", "vedha-probe").Run()
		exec.Command("systemctl", "disable", "vedha-probe").Run()
		os.Remove(systemdService)
		os.Remove("/usr/local/bin/vedha-probe")
		exec.Command("systemctl", "daemon-reload").Run()
		fmt.Println("Probe service removed (Linux)")
	}
	return nil
}

func installLaunchd(binary, envFile string) error {
	plist := fmt.Sprintf(`<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>           <string>com.vedha.probe</string>
  <key>ProgramArguments</key>
  <array>
    <string>%s</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PROBE_ENV_FILE</key> <string>%s</string>
  </dict>
  <key>RunAtLoad</key>        <true/>
  <key>KeepAlive</key>        <true/>
  <key>StandardOutPath</key>  <string>/var/log/vedha-probe.log</string>
  <key>StandardErrorPath</key><string>/var/log/vedha-probe.log</string>
  <key>ThrottleInterval</key> <integer>10</integer>
</dict>
</plist>`, binary, envFile)

	if err := os.WriteFile(launchdPlist, []byte(plist), 0644); err != nil {
		return fmt.Errorf("cannot write plist (try sudo): %w", err)
	}

	// Load the service
	out, err := exec.Command("launchctl", "load", "-w", launchdPlist).CombinedOutput()
	if err != nil {
		return fmt.Errorf("launchctl load failed: %v\n%s", err, out)
	}
	fmt.Println("Probe service installed and started (macOS LaunchDaemon)")
	fmt.Printf("  Logs : tail -f /var/log/vedha-probe.log\n")
	fmt.Printf("  Stop : sudo launchctl unload %s\n", launchdPlist)
	return nil
}

func installSystemd(binary, envFile string) error {
	unit := fmt.Sprintf(`[Unit]
Description=Vedha Probe — Agentic VA Scanner
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=%s
Environment=PROBE_ENV_FILE=%s
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vedha-probe
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/vedha-probe /var/log

[Install]
WantedBy=multi-user.target
`, binary, envFile)

	if err := os.WriteFile(systemdService, []byte(unit), 0644); err != nil {
		return fmt.Errorf("cannot write service file (try sudo): %w", err)
	}

	cmds := [][]string{
		{"systemctl", "daemon-reload"},
		{"systemctl", "enable", "vedha-probe"},
		{"systemctl", "start", "vedha-probe"},
	}
	for _, c := range cmds {
		out, err := exec.Command(c[0], c[1:]...).CombinedOutput()
		if err != nil {
			return fmt.Errorf("%s failed: %v\n%s", strings.Join(c, " "), err, out)
		}
	}
	fmt.Println("Probe service installed and started (systemd)")
	fmt.Printf("  Status : systemctl status vedha-probe\n")
	fmt.Printf("  Logs   : journalctl -u vedha-probe -f\n")
	fmt.Printf("  Stop   : sudo systemctl stop vedha-probe\n")
	return nil
}

func copyFile(src, dst string) error {
	data, err := os.ReadFile(src)
	if err != nil {
		return err
	}
	return os.WriteFile(dst, data, 0755)
}
