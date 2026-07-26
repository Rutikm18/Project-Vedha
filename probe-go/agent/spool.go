// agent/spool.go — local result spool with retry.
// Saves results to disk when the manager is unreachable; flushes on next run.
package agent

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

type Spool struct {
	dir string
}

var safeJobID = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`)

func NewSpool(dir string) *Spool {
	return &Spool{dir: dir}
}

// Save writes a result to the spool directory (named by jobID).
func (s *Spool) Save(jobID string, payload interface{}) error {
	path, err := s.path(jobID)
	if err != nil {
		return err
	}
	b, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	if err := os.MkdirAll(s.dir, 0700); err != nil {
		return fmt.Errorf("create spool directory: %w", err)
	}
	if err := os.Chmod(s.dir, 0700); err != nil {
		return fmt.Errorf("secure spool directory: %w", err)
	}

	tmp, err := os.CreateTemp(s.dir, ".result-*.tmp")
	if err != nil {
		return fmt.Errorf("create spool temp file: %w", err)
	}
	tmpPath := tmp.Name()
	defer os.Remove(tmpPath)

	if err := tmp.Chmod(0600); err != nil {
		tmp.Close()
		return fmt.Errorf("secure spool temp file: %w", err)
	}
	if _, err := tmp.Write(b); err != nil {
		tmp.Close()
		return fmt.Errorf("write spool result: %w", err)
	}
	if err := tmp.Sync(); err != nil {
		tmp.Close()
		return fmt.Errorf("sync spool result: %w", err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("close spool result: %w", err)
	}
	if err := os.Rename(tmpPath, path); err != nil {
		return fmt.Errorf("commit spool result: %w", err)
	}
	return syncDir(s.dir)
}

// Delete removes a result only after the manager has acknowledged it.
func (s *Spool) Delete(jobID string) error {
	path, err := s.path(jobID)
	if err != nil {
		return err
	}
	if err := os.Remove(path); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("remove spooled result: %w", err)
	}
	return syncDir(s.dir)
}

// Flush re-submits all spooled results to the manager.
func (s *Spool) Flush(submit func(jobID string, payload map[string]interface{}) error) int {
	entries, err := os.ReadDir(s.dir)
	if err != nil {
		return 0
	}
	flushed := 0
	for _, e := range entries {
		if filepath.Ext(e.Name()) != ".json" {
			continue
		}
		path := filepath.Join(s.dir, e.Name())
		b, err := os.ReadFile(path)
		if err != nil {
			continue
		}
		var payload map[string]interface{}
		if err := json.Unmarshal(b, &payload); err != nil {
			continue
		}
		jobID := e.Name()[:len(e.Name())-5] // strip .json
		if _, err := s.path(jobID); err != nil {
			log.Printf("[spool] ignoring unsafe result filename %q: %v", e.Name(), err)
			continue
		}
		if err := submit(jobID, payload); err != nil {
			log.Printf("[spool] re-submit %s failed: %v", jobID, err)
			continue
		}
		if err := s.Delete(jobID); err != nil {
			log.Printf("[spool] acknowledged %s but cleanup failed: %v", jobID, err)
			continue
		}
		flushed++
	}
	return flushed
}

// Count returns the number of spooled results waiting.
func (s *Spool) Count() int {
	entries, _ := os.ReadDir(s.dir)
	n := 0
	for _, e := range entries {
		if filepath.Ext(e.Name()) == ".json" {
			n++
		}
	}
	return n
}

func (s *Spool) path(jobID string) (string, error) {
	if !safeJobID.MatchString(jobID) || strings.Contains(jobID, "..") {
		return "", fmt.Errorf("invalid job ID for spool: %q", jobID)
	}
	return filepath.Join(s.dir, jobID+".json"), nil
}

func syncDir(path string) error {
	dir, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("open spool directory for sync: %w", err)
	}
	defer dir.Close()
	if err := dir.Sync(); err != nil {
		return fmt.Errorf("sync spool directory: %w", err)
	}
	return nil
}
