package config

import (
	"os"
	"path/filepath"
	"testing"
)

func TestLoadEnvironmentOverridesEnvFile(t *testing.T) {
	t.Setenv("PROBE_NAME", "environment-probe")
	envFile := filepath.Join(t.TempDir(), "probe.env")
	if err := os.WriteFile(
		envFile,
		[]byte("PROBE_NAME=file-probe\n"),
		0600,
	); err != nil {
		t.Fatal(err)
	}

	cfg := Load(envFile)
	if cfg.ProbeName != "environment-probe" {
		t.Fatalf("PROBE_NAME = %q, want environment value", cfg.ProbeName)
	}
}
