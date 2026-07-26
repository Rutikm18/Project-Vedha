package agent

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"reflect"
	"sync"
	"testing"

	"probe-go/config"
)

type identityServerState struct {
	sync.Mutex
	loginCount    int
	registerCount int
	capabilities  []string
}

func newIdentityServer(t *testing.T) (*httptest.Server, *identityServerState) {
	t.Helper()
	state := &identityServerState{}
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/auth/login":
			state.Lock()
			state.loginCount++
			state.Unlock()
			writeJSON(t, w, map[string]string{"access_token": "operator-token"})
		case "/agents/register":
			var body struct {
				Capabilities []string `json:"capabilities"`
			}
			if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
				t.Errorf("decode register request: %v", err)
				http.Error(w, "bad request", http.StatusBadRequest)
				return
			}
			state.Lock()
			state.registerCount++
			state.capabilities = append([]string(nil), body.Capabilities...)
			state.Unlock()
			writeJSON(t, w, map[string]string{
				"agent_id": "registered-agent",
				"token":    "registered-token",
			})
		default:
			http.NotFound(w, r)
		}
	}))
	return server, state
}

func writeJSON(t *testing.T, w http.ResponseWriter, value interface{}) {
	t.Helper()
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(value); err != nil {
		t.Errorf("encode test response: %v", err)
	}
}

func identityTestConfig(serverURL, stateFile string) *config.Config {
	return &config.Config{
		PlatformURL:      serverURL,
		ProbeName:        "probe-a",
		OperatorEmail:    "operator@example.test",
		OperatorPassword: "secret",
		StateFile:        stateFile,
		SpoolDir:         filepath.Join(filepath.Dir(stateFile), "spool"),
		VerifyTLS:        true,
	}
}

func TestObtainIdentityPersistsAndReusesRegistration(t *testing.T) {
	server, serverState := newIdentityServer(t)
	defer server.Close()
	stateFile := filepath.Join(t.TempDir(), "private", "state.json")

	first := New(identityTestConfig(server.URL, stateFile))
	if err := first.obtainIdentity(context.Background()); err != nil {
		t.Fatalf("first identity: %v", err)
	}

	second := New(identityTestConfig(server.URL, stateFile))
	if err := second.obtainIdentity(context.Background()); err != nil {
		t.Fatalf("reused identity: %v", err)
	}
	if second.transport.AgentID != "registered-agent" ||
		second.transport.AgentToken != "registered-token" {
		t.Fatalf("unexpected reused identity: %#v", second.transport)
	}

	serverState.Lock()
	loginCount := serverState.loginCount
	registerCount := serverState.registerCount
	registeredCapabilities := append([]string(nil), serverState.capabilities...)
	serverState.Unlock()
	if loginCount != 1 || registerCount != 1 {
		t.Fatalf("restart re-registered: login=%d register=%d",
			loginCount, registerCount)
	}
	if !reflect.DeepEqual(registeredCapabilities, Capabilities) {
		t.Fatalf("registered capabilities mismatch:\n got %v\nwant %v",
			registeredCapabilities, Capabilities)
	}

	dirInfo, err := os.Stat(filepath.Dir(stateFile))
	if err != nil {
		t.Fatal(err)
	}
	fileInfo, err := os.Stat(stateFile)
	if err != nil {
		t.Fatal(err)
	}
	if got := dirInfo.Mode().Perm(); got != 0700 {
		t.Fatalf("state directory mode = %04o, want 0700", got)
	}
	if got := fileInfo.Mode().Perm(); got != 0600 {
		t.Fatalf("state file mode = %04o, want 0600", got)
	}
}

func TestObtainIdentityRecoversFromCorruptState(t *testing.T) {
	server, serverState := newIdentityServer(t)
	defer server.Close()
	stateDir := filepath.Join(t.TempDir(), "private")
	if err := os.MkdirAll(stateDir, 0700); err != nil {
		t.Fatal(err)
	}
	stateFile := filepath.Join(stateDir, "state.json")
	if err := os.WriteFile(stateFile, []byte(`{"agent_id":`), 0600); err != nil {
		t.Fatal(err)
	}

	agent := New(identityTestConfig(server.URL, stateFile))
	if err := agent.obtainIdentity(context.Background()); err != nil {
		t.Fatalf("recover corrupt state: %v", err)
	}

	serverState.Lock()
	loginCount := serverState.loginCount
	registerCount := serverState.registerCount
	serverState.Unlock()
	if loginCount != 1 || registerCount != 1 {
		t.Fatalf("corrupt state did not trigger registration: login=%d register=%d",
			loginCount, registerCount)
	}
	if _, err := loadIdentityState(stateFile, server.URL, "probe-a"); err != nil {
		t.Fatalf("replacement state is invalid: %v", err)
	}
}

func TestConfiguredIdentityTakesPrecedenceOverState(t *testing.T) {
	stateFile := filepath.Join(t.TempDir(), "state.json")
	if err := saveIdentityState(
		stateFile, "cached-agent", "cached-token",
		"http://manager.invalid", "probe-a",
	); err != nil {
		t.Fatal(err)
	}
	cfg := identityTestConfig("http://unused.invalid", stateFile)
	cfg.AgentID = "configured-agent"
	cfg.AgentToken = "configured-token"

	agent := New(cfg)
	if err := agent.obtainIdentity(context.Background()); err != nil {
		t.Fatalf("configured identity: %v", err)
	}
	if agent.transport.AgentID != "configured-agent" ||
		agent.transport.AgentToken != "configured-token" {
		t.Fatalf("state overrode configured identity")
	}
}

func TestConfiguredIdentityRejectsPartialCredentials(t *testing.T) {
	cfg := identityTestConfig("http://unused.invalid", "")
	cfg.AgentID = "configured-agent"

	err := New(cfg).obtainIdentity(context.Background())
	if err == nil {
		t.Fatal("expected partial credentials to fail")
	}
}

func TestIdentityStateRejectsDifferentManager(t *testing.T) {
	stateFile := filepath.Join(t.TempDir(), "state.json")
	if err := saveIdentityState(
		stateFile, "agent", "token", "https://manager-a.example", "probe-a",
	); err != nil {
		t.Fatal(err)
	}
	if _, err := loadIdentityState(
		stateFile, "https://manager-b.example", "probe-a",
	); err == nil {
		t.Fatal("expected manager-bound state to be rejected")
	}
}
