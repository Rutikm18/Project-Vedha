package scanner

import (
	"context"
	"net"
	"net/http"
	"net/http/httptest"
	"strconv"
	"sync/atomic"
	"testing"
	"time"
)

func TestProbeHTTPDoesNotFollowRedirects(t *testing.T) {
	t.Parallel()

	var redirectedHits atomic.Int32
	redirectTarget := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		redirectedHits.Add(1)
		w.WriteHeader(http.StatusOK)
	}))
	defer redirectTarget.Close()

	source := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, redirectTarget.URL, http.StatusFound)
	}))
	defer source.Close()

	host, portText, err := net.SplitHostPort(source.Listener.Addr().String())
	if err != nil {
		t.Fatalf("split source address: %v", err)
	}
	port, err := strconv.Atoi(portText)
	if err != nil {
		t.Fatalf("parse source port: %v", err)
	}

	result := ProbeHTTP(context.Background(), host, port, false, time.Second)

	if got := redirectedHits.Load(); got != 0 {
		t.Fatalf("redirect target received %d request(s); expected none", got)
	}
	if result.Status != "open" {
		t.Fatalf("status = %q, want open (error=%q)", result.Status, result.Error)
	}
	if got := result.Data["status"]; got != http.StatusFound {
		t.Fatalf("HTTP status = %#v, want %d", got, http.StatusFound)
	}
	if got := result.Data["redirect_location"]; got != redirectTarget.URL {
		t.Fatalf("redirect_location = %#v, want %q", got, redirectTarget.URL)
	}
}
