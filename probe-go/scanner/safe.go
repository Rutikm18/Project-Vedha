// scanner/safe.go — error-handling foundation for every scanner.
//
// Design goals (a probe runs unattended on customer infra — it must NEVER crash):
//   1. A panic in any single scanner becomes an error Result, not a dead process.
//   2. Transient network errors are retried with exponential backoff + jitter.
//   3. Every network op honours a hard deadline via context.
//   4. Repeated failures against one host trip a circuit breaker so a dead host
//      doesn't waste the whole scan budget.
package scanner

import (
	"context"
	"errors"
	"fmt"
	"math"
	"math/rand"
	"net"
	"runtime/debug"
	"strings"
	"sync"
	"time"
)

// SafeRun executes fn with panic recovery. A panic is converted into an error
// Result tagged with the scanner name and target so the pipeline keeps going.
func SafeRun(scannerName, target string, fn func() Result) (res Result) {
	defer func() {
		if r := recover(); r != nil {
			res = newResult(scannerName, target)
			res.Status = "error"
			res.Error = fmt.Sprintf("panic recovered: %v", r)
			res.Data["stack"] = string(debug.Stack())
		}
	}()
	return fn()
}

// SafeRunMulti is SafeRun for scanners that return several Results.
func SafeRunMulti(scannerName, target string, fn func() []Result) (out []Result) {
	defer func() {
		if r := recover(); r != nil {
			er := newResult(scannerName, target)
			er.Status = "error"
			er.Error = fmt.Sprintf("panic recovered: %v", r)
			out = []Result{er}
		}
	}()
	return fn()
}

// RetryConfig controls exponential-backoff retry behaviour.
type RetryConfig struct {
	MaxAttempts int
	BaseDelay   time.Duration
	MaxDelay    time.Duration
}

// DefaultRetry is a sensible default for network scanning: 3 attempts, fast backoff.
var DefaultRetry = RetryConfig{MaxAttempts: 3, BaseDelay: 150 * time.Millisecond, MaxDelay: 2 * time.Second}

// Retry runs fn until it succeeds, exhausts attempts, or ctx is cancelled.
// Only *transient* errors are retried — a connection refused (definitive
// "closed") returns immediately so we don't waste attempts on a closed port.
func Retry(ctx context.Context, cfg RetryConfig, fn func() error) error {
	if cfg.MaxAttempts < 1 {
		cfg.MaxAttempts = 1
	}
	var lastErr error
	for attempt := 0; attempt < cfg.MaxAttempts; attempt++ {
		if ctx.Err() != nil {
			return ctx.Err()
		}
		lastErr = fn()
		if lastErr == nil {
			return nil
		}
		if !IsTransient(lastErr) {
			return lastErr // definitive failure — don't retry
		}
		if attempt == cfg.MaxAttempts-1 {
			break
		}
		delay := backoff(cfg.BaseDelay, cfg.MaxDelay, attempt)
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(delay):
		}
	}
	return fmt.Errorf("after %d attempts: %w", cfg.MaxAttempts, lastErr)
}

func backoff(base, max time.Duration, attempt int) time.Duration {
	d := float64(base) * math.Pow(2, float64(attempt))
	d += rand.Float64() * float64(base) // jitter
	if d > float64(max) {
		d = float64(max)
	}
	return time.Duration(d)
}

// IsTransient reports whether an error is worth retrying (timeout, temporary
// network condition) versus definitive (connection refused, no route).
func IsTransient(err error) bool {
	if err == nil {
		return false
	}
	var netErr net.Error
	if errors.As(err, &netErr) && netErr.Timeout() {
		return true
	}
	s := strings.ToLower(err.Error())
	switch {
	case strings.Contains(s, "connection refused"):
		return false // port is definitively closed
	case strings.Contains(s, "no route to host"):
		return false
	case strings.Contains(s, "network is unreachable"):
		return false
	case strings.Contains(s, "timeout"),
		strings.Contains(s, "temporarily unavailable"),
		strings.Contains(s, "reset by peer"),
		strings.Contains(s, "broken pipe"),
		strings.Contains(s, "i/o timeout"):
		return true
	}
	return false
}

// IsRefused reports a definitive "closed port" — the host answered with RST.
// A refused connection still proves the host is ALIVE.
func IsRefused(err error) bool {
	if err == nil {
		return false
	}
	return strings.Contains(strings.ToLower(err.Error()), "connection refused")
}

// CircuitBreaker trips after N consecutive failures against a target so the
// pipeline stops hammering a dead/filtered host and moves on.
type CircuitBreaker struct {
	mu        sync.Mutex
	threshold int
	failures  map[string]int
	tripped   map[string]bool
}

func NewCircuitBreaker(threshold int) *CircuitBreaker {
	if threshold < 1 {
		threshold = 5
	}
	return &CircuitBreaker{
		threshold: threshold,
		failures:  make(map[string]int),
		tripped:   make(map[string]bool),
	}
}

// Allow reports whether more probes to host are permitted.
func (c *CircuitBreaker) Allow(host string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return !c.tripped[host]
}

// RecordSuccess resets the failure counter for a host.
func (c *CircuitBreaker) RecordSuccess(host string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.failures[host] = 0
}

// RecordFailure increments the failure counter and trips the breaker at threshold.
func (c *CircuitBreaker) RecordFailure(host string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.failures[host]++
	if c.failures[host] >= c.threshold {
		c.tripped[host] = true
	}
}

// Tripped returns the list of hosts whose breaker has opened (for run stats).
func (c *CircuitBreaker) Tripped() []string {
	c.mu.Lock()
	defer c.mu.Unlock()
	var out []string
	for h, t := range c.tripped {
		if t {
			out = append(out, h)
		}
	}
	return out
}

// DialContext is the single hardened dial used by every TCP scanner. It applies
// the timeout, retries transient failures, and classifies the outcome.
func DialContext(ctx context.Context, network, addr string, timeout time.Duration) (net.Conn, error) {
	var conn net.Conn
	err := Retry(ctx, DefaultRetry, func() error {
		d := &net.Dialer{}
		dctx, cancel := context.WithTimeout(ctx, timeout)
		defer cancel()
		c, e := d.DialContext(dctx, network, addr)
		if e != nil {
			return e
		}
		conn = c
		return nil
	})
	return conn, err
}
