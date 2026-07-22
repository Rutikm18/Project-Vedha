// agent/spool.go — local result spool with retry.
// Saves results to disk when the manager is unreachable; flushes on next run.
package agent

import (
	"encoding/json"
	"log"
	"os"
	"path/filepath"
)

type Spool struct {
	dir string
}

func NewSpool(dir string) *Spool {
	os.MkdirAll(dir, 0700)
	return &Spool{dir: dir}
}

// Save writes a result to the spool directory (named by jobID).
func (s *Spool) Save(jobID string, payload interface{}) error {
	b, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	path := filepath.Join(s.dir, jobID+".json")
	return os.WriteFile(path, b, 0600)
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
		if err := submit(jobID, payload); err != nil {
			log.Printf("[spool] re-submit %s failed: %v", jobID, err)
			continue
		}
		os.Remove(path)
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
