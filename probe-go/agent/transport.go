// agent/transport.go — HTTP client + WebSocket to the manager.
package agent

import (
	"bytes"
	"context"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/gorilla/websocket"
)

type Transport struct {
	baseURL    string
	client     *http.Client
	verifyTLS  bool
	AgentID    string
	AgentToken string
}

func NewTransport(platformURL string, verifyTLS bool) *Transport {
	tr := &http.Transport{
		TLSClientConfig: managerTLSConfig(verifyTLS),
	}
	return &Transport{
		baseURL:   platformURL,
		client:    &http.Client{Transport: tr, Timeout: 30 * time.Second},
		verifyTLS: verifyTLS,
	}
}

func managerTLSConfig(verifyTLS bool) *tls.Config {
	return &tls.Config{
		MinVersion:         tls.VersionTLS12,
		InsecureSkipVerify: !verifyTLS, // Explicit opt-out via VERIFY_TLS=false.
	}
}

// Login authenticates the operator and returns an operator JWT.
func (t *Transport) Login(email, password string) (string, error) {
	var resp struct {
		AccessToken string `json:"access_token"`
	}
	if err := t.post("/auth/login", map[string]string{"email": email, "password": password}, &resp, ""); err != nil {
		return "", err
	}
	return resp.AccessToken, nil
}

// Register registers the probe as an agent and persists the returned identity.
func (t *Transport) Register(operatorToken, name, location string, caps, segments []string) error {
	body := map[string]interface{}{
		"name":             name,
		"location":         location,
		"capabilities":     caps,
		"network_segments": segments,
	}
	var resp struct {
		AgentID string `json:"agent_id"`
		Token   string `json:"token"`
	}
	if err := t.post("/agents/register", body, &resp, operatorToken); err != nil {
		return err
	}
	t.AgentID = strings.TrimSpace(resp.AgentID)
	t.AgentToken = strings.TrimSpace(resp.Token)
	if t.AgentID == "" || t.AgentToken == "" {
		t.AgentID = ""
		t.AgentToken = ""
		return fmt.Errorf("register response omitted agent_id or token")
	}
	return nil
}

// Heartbeat sends status to the manager and renews the active job lease.
func (t *Transport) Heartbeat(ctx context.Context, status, currentJobID string) error {
	body := map[string]interface{}{
		"agent_id": t.AgentID,
		"status":   status,
	}
	if currentJobID != "" {
		body["current_job_id"] = currentJobID
	} else {
		body["current_job_id"] = nil
	}
	return t.postContext(ctx, "/agents/heartbeat", body, nil, t.AgentToken)
}

// RefreshRegistration replaces stale capability and routing metadata.
func (t *Transport) RefreshRegistration(caps, segments []string) error {
	body := map[string]interface{}{
		"capabilities":     caps,
		"network_segments": segments,
	}
	return t.post(
		fmt.Sprintf("/agents/%s/refresh", t.AgentID),
		body, nil, t.AgentToken,
	)
}

// PollJobs fetches pending jobs for this agent.
func (t *Transport) PollJobs(limit int) ([]map[string]interface{}, error) {
	path := fmt.Sprintf("/agents/%s/jobs?limit=%d&status=pending", t.AgentID, limit)
	var jobs []map[string]interface{}
	err := t.get(path, &jobs, t.AgentToken)
	return jobs, err
}

// SubmitResult posts the scan result for a job.
func (t *Transport) SubmitResult(jobID string, payload interface{}) error {
	path := fmt.Sprintf("/agents/%s/jobs/%s/result", t.AgentID, jobID)
	return t.post(path, payload, nil, t.AgentToken)
}

// ConnectWS opens a WebSocket to the manager's push endpoint.
func (t *Transport) ConnectWS() (*websocket.Conn, error) {
	if t.AgentToken == "" {
		return nil, fmt.Errorf("cannot connect WebSocket without an agent token")
	}
	u, err := url.Parse(t.baseURL)
	if err != nil {
		return nil, err
	}
	switch u.Scheme {
	case "https":
		u.Scheme = "wss"
	default:
		u.Scheme = "ws"
	}
	u.Path = "/agents/ws"
	query := u.Query()
	query.Set("token", t.AgentToken)
	u.RawQuery = query.Encode()

	dialer := websocket.Dialer{
		TLSClientConfig:  managerTLSConfig(t.verifyTLS),
		HandshakeTimeout: 10 * time.Second,
	}
	conn, _, err := dialer.Dial(u.String(), nil)
	return conn, err
}

// ── low-level HTTP helpers ────────────────────────────────────────────────────

func (t *Transport) get(path string, out interface{}, token string) error {
	req, err := http.NewRequest("GET", t.baseURL+path, nil)
	if err != nil {
		return err
	}
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	resp, err := t.client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 400 {
		b, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("GET %s: HTTP %d — %s", path, resp.StatusCode, b)
	}
	return json.NewDecoder(resp.Body).Decode(out)
}

func (t *Transport) post(path string, body interface{}, out interface{}, token string) error {
	return t.postContext(context.Background(), path, body, out, token)
}

func (t *Transport) postContext(
	ctx context.Context,
	path string,
	body interface{},
	out interface{},
	token string,
) error {
	b, err := json.Marshal(body)
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, "POST", t.baseURL+path, bytes.NewReader(b))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	resp, err := t.client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	rb, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 400 {
		return fmt.Errorf("POST %s: HTTP %d — %s", path, resp.StatusCode, rb)
	}
	if out != nil {
		return json.Unmarshal(rb, out)
	}
	return nil
}
