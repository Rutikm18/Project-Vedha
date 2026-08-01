package agent

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"
	"time"

	"github.com/gorilla/websocket"
)

func TestConnectWSHonorsTLSVerificationAndManagerEndpoint(t *testing.T) {
	observed := make(chan struct {
		path          string
		rawQuery      string
		authorization string
	}, 1)
	upgrader := websocket.Upgrader{}
	server := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		observed <- struct {
			path          string
			rawQuery      string
			authorization string
		}{
			path:          r.URL.Path,
			rawQuery:      r.URL.RawQuery,
			authorization: r.Header.Get("Authorization"),
		}
		conn, err := upgrader.Upgrade(w, r, nil)
		if err == nil {
			_ = conn.Close()
		}
	}))
	server.Config.ErrorLog = log.New(io.Discard, "", 0)
	server.StartTLS()
	defer server.Close()

	strict := NewTransport(server.URL, true)
	strict.AgentToken = "test-token"
	if conn, err := strict.ConnectWS(); err == nil {
		_ = conn.Close()
		t.Fatal("strict TLS accepted the untrusted test certificate")
	}

	insecure := NewTransport(server.URL, false)
	insecure.AgentToken = "test-token"
	conn, err := insecure.ConnectWS()
	if err != nil {
		t.Fatalf("explicit TLS verification opt-out did not connect: %v", err)
	}
	_ = conn.Close()

	select {
	case got := <-observed:
		if got.path != "/agents/ws" {
			t.Fatalf("WebSocket path = %q, want /agents/ws", got.path)
		}
		if got.rawQuery != "" {
			t.Fatalf("WebSocket query leaked credentials: %q", got.rawQuery)
		}
		if got.authorization != "Bearer test-token" {
			t.Fatalf("WebSocket Authorization = %q, want Bearer test-token", got.authorization)
		}
	case <-time.After(time.Second):
		t.Fatal("WebSocket server did not observe the connection")
	}
}

func TestHeartbeatUsesManagerContractAndRetriesFailures(t *testing.T) {
	type observedRequest struct {
		method        string
		path          string
		authorization string
		body          map[string]interface{}
	}

	var attempts atomic.Int32
	observed := make(chan observedRequest, 3)
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var body map[string]interface{}
		_ = json.NewDecoder(r.Body).Decode(&body)
		observed <- observedRequest{
			method:        r.Method,
			path:          r.URL.Path,
			authorization: r.Header.Get("Authorization"),
			body:          body,
		}
		if attempts.Add(1) < 3 {
			http.Error(w, "temporary failure", http.StatusServiceUnavailable)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer server.Close()

	transport := NewTransport(server.URL, true)
	transport.AgentID = "22222222-2222-2222-2222-222222222222"
	transport.AgentToken = "test-token"
	probe := &Agent{transport: transport}

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	err := probe.heartbeatWithRetry(
		ctx, "busy", "11111111-1111-1111-1111-111111111111", 3,
	)
	if err != nil {
		t.Fatalf("heartbeat retry did not recover: %v", err)
	}
	if got := attempts.Load(); got != 3 {
		t.Fatalf("heartbeat attempts = %d, want 3", got)
	}

	for i := 0; i < 3; i++ {
		request := <-observed
		if request.method != http.MethodPost || request.path != "/agents/heartbeat" {
			t.Fatalf("heartbeat request = %s %s, want POST /agents/heartbeat",
				request.method, request.path)
		}
		if request.authorization != "Bearer test-token" {
			t.Fatalf("authorization = %q", request.authorization)
		}
		if request.body["agent_id"] != transport.AgentID ||
			request.body["status"] != "busy" ||
			request.body["current_job_id"] != "11111111-1111-1111-1111-111111111111" {
			t.Fatalf("heartbeat body = %#v", request.body)
		}
	}
}
