package agent

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"
	"probe-go/config"
)

func TestWSJSONWriterSerializesConcurrentWrites(t *testing.T) {
	const messageCount = 64

	readDone := make(chan error, 1)
	upgrader := websocket.Upgrader{}
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			readDone <- err
			return
		}
		defer conn.Close()
		for i := 0; i < messageCount; i++ {
			var message map[string]interface{}
			if err := conn.ReadJSON(&message); err != nil {
				readDone <- err
				return
			}
		}
		readDone <- nil
	}))
	defer server.Close()

	transport := NewTransport(server.URL, true)
	transport.AgentToken = "test-token"
	conn, err := transport.ConnectWS()
	if err != nil {
		t.Fatalf("connect WebSocket: %v", err)
	}
	defer conn.Close()

	writer := &wsJSONWriter{conn: conn, timeout: time.Second}
	errs := make(chan error, messageCount)
	var wg sync.WaitGroup
	for i := 0; i < messageCount; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			if err := writer.Write(map[string]interface{}{"sequence": n}); err != nil {
				errs <- err
			}
		}(i)
	}
	wg.Wait()
	close(errs)
	for err := range errs {
		t.Errorf("concurrent write failed: %v", err)
	}

	select {
	case err := <-readDone:
		if err != nil {
			t.Fatalf("server read concurrent writes: %v", err)
		}
	case <-time.After(2 * time.Second):
		t.Fatal("server did not receive all serialized messages")
	}
}

func TestWSSessionRequiresAtomicClaimFeature(t *testing.T) {
	upgrader := websocket.Upgrader{}
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}
		defer conn.Close()

		var hello wsHelloMessage
		if err := conn.ReadJSON(&hello); err != nil {
			return
		}
		_ = conn.WriteJSON(map[string]interface{}{
			"type": "hello_ok", "protocol_version": wsProtocolVersion, "features": []string{},
		})
	}))
	defer server.Close()

	cfg := &config.Config{
		PlatformURL: server.URL, ProbeName: "test-probe", VerifyTLS: true,
		HeartbeatInterval: time.Hour, SpoolDir: t.TempDir(),
	}
	agent := New(cfg)
	agent.transport.AgentID = "22222222-2222-2222-2222-222222222222"
	agent.transport.AgentToken = "test-token"

	if err := agent.wsSession(context.Background()); err != errWSFallback {
		t.Fatalf("wsSession error = %v, want HTTP fallback sentinel", err)
	}
}

func TestWSSessionExecutesOnlyAfterPositiveClaim(t *testing.T) {
	const jobID = "11111111-1111-1111-1111-111111111111"

	for _, tc := range []struct {
		name       string
		claimed    bool
		wantResult bool
	}{
		{name: "claim_confirmed", claimed: true, wantResult: true},
		{name: "claim_rejected", claimed: false, wantResult: false},
	} {
		t.Run(tc.name, func(t *testing.T) {
			offerAcked := make(chan struct{}, 1)
			sendClaim := make(chan struct{})
			resultSeen := make(chan struct{}, 1)
			handlerDone := make(chan error, 1)
			releaseServer := make(chan struct{})
			upgrader := websocket.Upgrader{}

			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				conn, err := upgrader.Upgrade(w, r, nil)
				if err != nil {
					handlerDone <- err
					return
				}
				defer conn.Close()

				var hello wsHelloMessage
				if err := conn.ReadJSON(&hello); err != nil {
					handlerDone <- err
					return
				}
				if hello.Type != "hello" ||
					hello.ProtocolVersion != wsProtocolVersion ||
					!containsString(hello.Features, wsAtomicClaimFeature) {
					handlerDone <- fmt.Errorf("unexpected hello: %#v", hello)
					return
				}
				if err := conn.WriteJSON(map[string]interface{}{
					"type":             "hello_ok",
					"protocol_version": wsProtocolVersion,
					"features":         []string{wsAtomicClaimFeature},
				}); err != nil {
					handlerDone <- err
					return
				}
				if err := conn.WriteJSON(map[string]interface{}{
					"type": "job_push",
					"job": map[string]interface{}{
						"job_id":   jobID,
						"job_type": "assessment",
						"params": map[string]interface{}{
							"use_case_id":  "uc_ot_passive",
							"targets":      []string{"192.0.2.10"},
							"_scope_cidrs": []string{"192.0.2.0/24"},
						},
					},
				}); err != nil {
					handlerDone <- err
					return
				}

				for {
					var message map[string]interface{}
					if err := conn.ReadJSON(&message); err != nil {
						handlerDone <- err
						return
					}
					if message["type"] != "job_ack" {
						continue
					}
					if accepted, _ := message["accepted"].(bool); !accepted {
						handlerDone <- fmt.Errorf("job offer was unexpectedly declined")
						return
					}
					offerAcked <- struct{}{}
					break
				}

				<-sendClaim
				if err := conn.WriteJSON(map[string]interface{}{
					"type": "job_claim", "job_id": jobID,
					"claimed": tc.claimed, "reason": "test",
				}); err != nil {
					handlerDone <- err
					return
				}

				if tc.claimed {
					for {
						var message map[string]interface{}
						if err := conn.ReadJSON(&message); err != nil {
							handlerDone <- err
							return
						}
						if message["type"] == "result" {
							resultSeen <- struct{}{}
							break
						}
					}
				}
				if err := conn.WriteJSON(map[string]interface{}{
					"type": "displaced", "message": "test complete",
				}); err != nil {
					handlerDone <- err
					return
				}
				handlerDone <- nil
				<-releaseServer
			}))
			defer server.Close()
			defer close(releaseServer)

			cfg := &config.Config{
				PlatformURL: server.URL, ProbeName: "test-probe", VerifyTLS: true,
				HeartbeatInterval: time.Hour, SpoolDir: t.TempDir(),
			}
			agent := New(cfg)
			agent.transport.AgentID = "22222222-2222-2222-2222-222222222222"
			agent.transport.AgentToken = "test-token"

			ctx, cancel := context.WithCancel(context.Background())
			defer cancel()
			sessionDone := make(chan error, 1)
			go func() {
				sessionDone <- agent.wsSession(ctx)
			}()

			select {
			case <-offerAcked:
			case err := <-handlerDone:
				t.Fatalf("WebSocket server failed before offer acknowledgment: %v", err)
			case <-time.After(time.Second):
				t.Fatal("probe did not acknowledge the staged offer")
			}

			time.Sleep(75 * time.Millisecond)
			if got := agent.spool.Count(); got != 0 {
				t.Fatalf("probe executed before job_claim; spool count = %d", got)
			}
			select {
			case <-resultSeen:
				t.Fatal("probe sent a result before job_claim")
			default:
			}

			close(sendClaim)
			select {
			case <-sessionDone:
			case <-time.After(2 * time.Second):
				cancel()
				t.Fatal("WebSocket session did not finish after claim decision")
			}
			select {
			case err := <-handlerDone:
				if err != nil {
					t.Fatalf("WebSocket server failed: %v", err)
				}
			case <-time.After(time.Second):
				t.Fatal("WebSocket server did not finish claim exchange")
			}

			select {
			case <-resultSeen:
				if !tc.wantResult {
					t.Fatal("probe executed a rejected claim")
				}
			default:
				if tc.wantResult {
					t.Fatal("probe did not execute a confirmed claim")
				}
			}
			if got := agent.spool.Count(); got != boolToInt(tc.wantResult) {
				t.Fatalf("spool count = %d, want %d", got, boolToInt(tc.wantResult))
			}
		})
	}
}

func TestWSSessionRetainsResultUntilMatchingAck(t *testing.T) {
	const jobID = "11111111-1111-1111-1111-111111111111"
	for _, tc := range []struct {
		name          string
		ackJobID      string
		wantSpoolSize int
	}{
		{name: "acknowledged", ackJobID: jobID, wantSpoolSize: 0},
		{name: "mismatched_ack", ackJobID: "33333333-3333-3333-3333-333333333333", wantSpoolSize: 1},
		{name: "connection_lost_before_ack", wantSpoolSize: 1},
	} {
		t.Run(tc.name, func(t *testing.T) {
			releaseServer := make(chan struct{})
			resultSeen := make(chan map[string]interface{}, 1)
			handlerErr := make(chan error, 1)
			upgrader := websocket.Upgrader{}

			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				conn, err := upgrader.Upgrade(w, r, nil)
				if err != nil {
					handlerErr <- err
					return
				}
				defer conn.Close()

				if err := conn.WriteJSON(map[string]interface{}{
					"type":             "hello_ok",
					"protocol_version": wsProtocolVersion,
					"features":         []string{wsAtomicClaimFeature},
				}); err != nil {
					handlerErr <- err
					return
				}
				if err := conn.WriteJSON(map[string]interface{}{
					"type": "job_push",
					"job": map[string]interface{}{
						"job_id":   jobID,
						"job_type": "assessment",
						"params": map[string]interface{}{
							"use_case_id":  "uc_ot_passive",
							"targets":      []string{"192.0.2.10"},
							"_scope_cidrs": []string{"192.0.2.0/24"},
						},
					},
				}); err != nil {
					handlerErr <- err
					return
				}

				for {
					var message map[string]interface{}
					if err := conn.ReadJSON(&message); err != nil {
						handlerErr <- err
						return
					}
					if message["type"] == "job_ack" {
						if accepted, _ := message["accepted"].(bool); !accepted {
							handlerErr <- fmt.Errorf("job offer was unexpectedly declined")
							return
						}
						if err := conn.WriteJSON(map[string]interface{}{
							"type": "job_claim", "job_id": jobID, "claimed": true,
						}); err != nil {
							handlerErr <- err
							return
						}
						continue
					}
					if message["type"] != "result" {
						continue
					}
					resultSeen <- message
					if tc.ackJobID != "" {
						if err := conn.WriteJSON(map[string]interface{}{
							"type": "result_ack", "job_id": tc.ackJobID,
						}); err != nil {
							handlerErr <- err
							return
						}
					}
					if err := conn.WriteJSON(map[string]interface{}{
						"type": "displaced", "message": "test complete",
					}); err != nil {
						handlerErr <- err
						return
					}
					<-releaseServer
					return
				}
			}))
			defer server.Close()
			defer close(releaseServer)

			cfg := &config.Config{
				PlatformURL:       server.URL,
				ProbeName:         "test-probe",
				VerifyTLS:         true,
				HeartbeatInterval: time.Hour,
				SpoolDir:          t.TempDir(),
			}
			agent := New(cfg)
			agent.transport.AgentID = "22222222-2222-2222-2222-222222222222"
			agent.transport.AgentToken = "test-token"

			ctx, cancel := context.WithCancel(context.Background())
			defer cancel()
			sessionDone := make(chan error, 1)
			go func() {
				sessionDone <- agent.wsSession(ctx)
			}()

			select {
			case <-sessionDone:
			case <-time.After(time.Second):
				cancel()
				select {
				case <-sessionDone:
				case <-time.After(3 * time.Second):
				}
				t.Fatal("WebSocket session shutdown waited for the heartbeat goroutine")
			}

			select {
			case message := <-resultSeen:
				if message["job_id"] != jobID {
					t.Fatalf("result job_id = %#v, want %s", message["job_id"], jobID)
				}
				if _, ok := message["success"].(bool); !ok {
					t.Fatalf("result success field is not boolean: %#v", message)
				}
				if _, ok := message["result"].(map[string]interface{}); !ok {
					t.Fatalf("result payload is not an object: %#v", message)
				}
			default:
				t.Fatal("manager did not receive a result frame")
			}

			if got := agent.spool.Count(); got != tc.wantSpoolSize {
				t.Fatalf("spool count = %d, want %d", got, tc.wantSpoolSize)
			}
			if tc.wantSpoolSize == 1 {
				path, err := agent.spool.path(jobID)
				if err != nil {
					t.Fatalf("spool path: %v", err)
				}
				raw, err := json.Marshal(readJSONFile(t, path))
				if err != nil {
					t.Fatalf("marshal retained payload: %v", err)
				}
				if len(raw) == 0 {
					t.Fatal("retained payload is empty")
				}
			}

			select {
			case err := <-handlerErr:
				t.Fatalf("WebSocket test server failed: %v", err)
			default:
			}
		})
	}
}

func boolToInt(value bool) int {
	if value {
		return 1
	}
	return 0
}

func readJSONFile(t *testing.T, path string) map[string]interface{} {
	t.Helper()

	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read retained payload: %v", err)
	}
	var payload map[string]interface{}
	if err := json.Unmarshal(data, &payload); err != nil {
		t.Fatalf("decode retained payload: %v", err)
	}
	if _, ok := payload["success"]; !ok {
		t.Fatalf("retained payload lacks success field: %#v", payload)
	}
	if _, ok := payload["result"]; !ok {
		t.Fatalf("retained payload lacks result field: %#v", payload)
	}
	return payload
}

func TestResultPayloadWrapsManagerContract(t *testing.T) {
	result := map[string]interface{}{"ok": false, "error": "scan failed"}
	payload := resultPayload(result)

	if payload["success"] != false {
		t.Fatalf("success = %#v, want false", payload["success"])
	}
	if payload["result"] == nil {
		t.Fatal("result payload is missing")
	}
	if got := fmt.Sprint(payload["error"]); got != "scan failed" {
		t.Fatalf("error = %q, want scan failed", got)
	}
}
