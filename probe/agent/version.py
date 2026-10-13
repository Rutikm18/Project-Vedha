"""The agent's own version. Bump it by hand whenever agent code changes.

This is NOT the platform release (the repo-root VERSION file, which the release
script uses to name a release directory): the agent has its own number so a
manager release that does not touch the agent does not look like an agent update.

It is a plain module so the compiled and container builds carry it with no data
file, and so scripts/agent_release.py can read it without importing the agent.
tools/check_agent_version.py (run in CI) fails a change that alters the agent's
code without changing this value.
"""

AGENT_VERSION = "2.2.9"
