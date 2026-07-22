// config/config.go — load probe configuration from env vars + probe.env file.
// Drop probe.env next to the binary; env vars override file values.
package config

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"time"
)

type Config struct {
	PlatformURL       string
	ProbeName         string
	ProbeLocation     string
	NetworkSegments   []string
	OperatorEmail     string
	OperatorPassword  string
	AgentID           string
	AgentToken        string
	HeartbeatInterval time.Duration
	PollInterval      time.Duration
	JobLimit          int
	VerifyTLS         bool
	StateFile         string
	SpoolDir          string
	WSEnabled         bool
	Profile           string // it | ot | iot
}

func Load(envFile string) *Config {
	loadFile(envFile)

	c := &Config{
		PlatformURL:       env("PLATFORM_URL", ""),
		ProbeName:         env("PROBE_NAME", hostname()),
		ProbeLocation:     env("PROBE_LOCATION", ""),
		OperatorEmail:     env("OPERATOR_EMAIL", ""),
		OperatorPassword:  env("OPERATOR_PASSWORD", ""),
		AgentID:           env("AGENT_ID", ""),
		AgentToken:        env("AGENT_TOKEN", ""),
		HeartbeatInterval: envDuration("HEARTBEAT_INTERVAL", 30*time.Second),
		PollInterval:      envDuration("POLL_INTERVAL", 10*time.Second),
		JobLimit:          envInt("JOB_LIMIT", 1),
		VerifyTLS:         envBool("VERIFY_TLS", true),
		StateFile:         env("STATE_FILE", "/var/lib/vedha-probe/state.json"),
		SpoolDir:          env("RESULT_SPOOL_DIR", "/var/lib/vedha-probe/spool"),
		WSEnabled:         envBool("PROBE_WS_ENABLED", true),
		Profile:           env("PROBE_PROFILE", "it"),
	}

	segs := env("PROBE_NETWORK_SEGMENTS", "")
	for _, s := range strings.Split(segs, ",") {
		if s = strings.TrimSpace(s); s != "" {
			c.NetworkSegments = append(c.NetworkSegments, s)
		}
	}
	return c
}

// loadFile reads key=value pairs from path into os.Environ (setenv only if
// not already set — env vars always win over the file).
func loadFile(path string) {
	f, err := os.Open(path)
	if err != nil {
		return
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		k, v, ok := strings.Cut(line, "=")
		if !ok {
			continue
		}
		k = strings.TrimSpace(k)
		v = strings.Trim(strings.TrimSpace(v), `"'`)
		os.Setenv(k, v) // Setenv (not LookupEnv + Setenv) always wins; we want file < env priority
	}
}

func env(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func envInt(key string, def int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return def
}

func envBool(key string, def bool) bool {
	v := strings.ToLower(os.Getenv(key))
	if v == "" {
		return def
	}
	return v != "false" && v != "0" && v != "no"
}

func envDuration(key string, def time.Duration) time.Duration {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return time.Duration(n) * time.Second
		}
	}
	return def
}

func hostname() string {
	h, _ := os.Hostname()
	return h
}
