package agent

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

type identityState struct {
	AgentID string
	Token   string
}

func loadIdentityState(path, platformURL, probeName string) (identityState, error) {
	var state identityState
	if strings.TrimSpace(path) == "" {
		return state, fs.ErrNotExist
	}

	info, err := os.Lstat(path)
	if err != nil {
		return state, err
	}
	if !info.Mode().IsRegular() {
		return state, fmt.Errorf("state file is not a regular file")
	}
	if err := secureStatePath(path); err != nil {
		return state, err
	}

	raw, err := os.ReadFile(path)
	if err != nil {
		return state, fmt.Errorf("read state file: %w", err)
	}
	var stored map[string]interface{}
	if err := json.Unmarshal(raw, &stored); err != nil {
		return state, fmt.Errorf("decode state file: %w", err)
	}

	state.AgentID, _ = stored["agent_id"].(string)
	state.Token, _ = stored["token"].(string)
	state.AgentID = strings.TrimSpace(state.AgentID)
	state.Token = strings.TrimSpace(state.Token)
	if state.AgentID == "" || state.Token == "" {
		return identityState{}, fmt.Errorf("state file has incomplete agent credentials")
	}

	if boundURL, ok := stored["platform_url"].(string); ok &&
		strings.TrimRight(strings.TrimSpace(boundURL), "/") !=
			strings.TrimRight(strings.TrimSpace(platformURL), "/") {
		return identityState{}, fmt.Errorf("state file belongs to a different manager")
	}
	if boundName, ok := stored["probe_name"].(string); ok &&
		strings.TrimSpace(boundName) != "" &&
		strings.TrimSpace(boundName) != strings.TrimSpace(probeName) {
		return identityState{}, fmt.Errorf("state file belongs to probe %q", boundName)
	}
	return state, nil
}

func saveIdentityState(path, agentID, token, platformURL, probeName string) error {
	agentID = strings.TrimSpace(agentID)
	token = strings.TrimSpace(token)
	if agentID == "" || token == "" {
		return fmt.Errorf("refusing to persist incomplete agent credentials")
	}

	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0700); err != nil {
		return fmt.Errorf("create state directory: %w", err)
	}
	if err := secureStateDirectory(dir); err != nil {
		return err
	}

	stored := make(map[string]interface{})
	if raw, err := os.ReadFile(path); err == nil {
		if err := json.Unmarshal(raw, &stored); err != nil {
			stored = make(map[string]interface{})
		}
	} else if !errors.Is(err, fs.ErrNotExist) {
		return fmt.Errorf("read existing state: %w", err)
	}
	if stored == nil {
		stored = make(map[string]interface{})
	}
	stored["agent_id"] = agentID
	stored["token"] = token
	stored["platform_url"] = strings.TrimRight(strings.TrimSpace(platformURL), "/")
	stored["probe_name"] = strings.TrimSpace(probeName)

	raw, err := json.Marshal(stored)
	if err != nil {
		return fmt.Errorf("encode state file: %w", err)
	}
	raw = append(raw, '\n')

	tmp, err := os.CreateTemp(dir, "."+filepath.Base(path)+".*.tmp")
	if err != nil {
		return fmt.Errorf("create state temp file: %w", err)
	}
	tmpPath := tmp.Name()
	defer os.Remove(tmpPath)

	closeWithError := func(cause error) error {
		if closeErr := tmp.Close(); cause == nil {
			cause = closeErr
		}
		return cause
	}
	if err := tmp.Chmod(0600); err != nil {
		return fmt.Errorf("secure state temp file: %w", closeWithError(err))
	}
	if _, err := tmp.Write(raw); err != nil {
		return fmt.Errorf("write state temp file: %w", closeWithError(err))
	}
	if err := tmp.Sync(); err != nil {
		return fmt.Errorf("sync state temp file: %w", closeWithError(err))
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("close state temp file: %w", err)
	}
	if err := os.Rename(tmpPath, path); err != nil {
		return fmt.Errorf("commit state file: %w", err)
	}
	if err := os.Chmod(path, 0600); err != nil {
		return fmt.Errorf("secure state file: %w", err)
	}
	return syncStateDirectory(dir)
}

func secureStatePath(path string) error {
	if err := secureStateDirectory(filepath.Dir(path)); err != nil {
		return err
	}
	if err := os.Chmod(path, 0600); err != nil {
		return fmt.Errorf("secure state file: %w", err)
	}
	return nil
}

func secureStateDirectory(dir string) error {
	info, err := os.Lstat(dir)
	if err != nil {
		return fmt.Errorf("inspect state directory: %w", err)
	}
	if !info.IsDir() {
		return fmt.Errorf("state parent is not a directory")
	}
	if err := os.Chmod(dir, 0700); err != nil {
		return fmt.Errorf("secure state directory: %w", err)
	}
	return nil
}

func syncStateDirectory(dir string) error {
	handle, err := os.Open(dir)
	if err != nil {
		return fmt.Errorf("open state directory for sync: %w", err)
	}
	defer handle.Close()
	if err := handle.Sync(); err != nil {
		return fmt.Errorf("sync state directory: %w", err)
	}
	return nil
}
