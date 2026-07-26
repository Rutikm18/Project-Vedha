package agent

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestSpoolSaveIsAtomicAndRejectsTraversal(t *testing.T) {
	t.Parallel()

	dir := filepath.Join(t.TempDir(), "spool")
	if err := os.Mkdir(dir, 0755); err != nil {
		t.Fatalf("create permissive spool directory: %v", err)
	}
	spool := NewSpool(dir)
	payload := map[string]interface{}{
		"success": true,
		"result":  map[string]interface{}{"ok": true},
	}

	if err := spool.Save("job-123", payload); err != nil {
		t.Fatalf("save result: %v", err)
	}

	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("read spool directory: %v", err)
	}
	if len(entries) != 1 || entries[0].Name() != "job-123.json" {
		t.Fatalf("spool entries = %v, want only job-123.json", entryNames(entries))
	}
	info, err := entries[0].Info()
	if err != nil {
		t.Fatalf("stat spool result: %v", err)
	}
	if got := info.Mode().Perm(); got != 0600 {
		t.Fatalf("spool permissions = %o, want 600", got)
	}
	dirInfo, err := os.Stat(dir)
	if err != nil {
		t.Fatalf("stat spool directory: %v", err)
	}
	if got := dirInfo.Mode().Perm(); got != 0700 {
		t.Fatalf("spool directory permissions = %o, want 700", got)
	}

	if err := spool.Save("../../outside", payload); err == nil {
		t.Fatal("path-traversal job ID was accepted")
	}
	if _, err := os.Stat(filepath.Join(dir, "..", "..", "outside.json")); !os.IsNotExist(err) {
		t.Fatalf("path traversal created an outside file: %v", err)
	}
}

func TestSpoolFlushDeletesOnlyAcknowledgedResults(t *testing.T) {
	t.Parallel()

	spool := NewSpool(t.TempDir())
	for _, jobID := range []string{"accepted-job", "retry-job"} {
		if err := spool.Save(jobID, map[string]interface{}{"job": jobID}); err != nil {
			t.Fatalf("save %s: %v", jobID, err)
		}
	}

	flushed := spool.Flush(func(jobID string, payload map[string]interface{}) error {
		if jobID == "retry-job" {
			return errors.New("manager unavailable")
		}
		return nil
	})

	if flushed != 1 {
		t.Fatalf("flushed = %d, want 1", flushed)
	}
	if got := spool.Count(); got != 1 {
		t.Fatalf("remaining spool count = %d, want 1", got)
	}
	if _, err := os.Stat(filepath.Join(spool.dir, "retry-job.json")); err != nil {
		t.Fatalf("retry result was not retained: %v", err)
	}
	if _, err := os.Stat(filepath.Join(spool.dir, "accepted-job.json")); !os.IsNotExist(err) {
		t.Fatalf("acknowledged result was not removed: %v", err)
	}
}

func entryNames(entries []os.DirEntry) []string {
	names := make([]string, 0, len(entries))
	for _, entry := range entries {
		names = append(names, entry.Name())
	}
	return names
}
