# Go Probe parity workspace

`probe-go/` is **not a supported Vedha product probe**. The only production
probe is [`../probe/`](../probe/), which is what root Docker Compose, bootstrap
scripts, documentation, and Manager compatibility tests deploy.

The Go implementation is retained as a migration workspace because a static Go
binary may become useful later. It must not be offered to operators or used for
production scanning until it has all of the following:

- every Manager use case, including SMB, SNMP, AI/MCP, passive OT, and the
  Manager-owned vulnerability-detection contract;
- encrypted scope delivery with the probe identity key;
- CA bundle and mutual-TLS support;
- PAT-only bootstrap plus the production license/hardware policy;
- durable result delivery and end-to-end parity tests against the Manager;
- the same controlled capability/accuracy validation gates as `../probe/`.

Today it intentionally has no root Compose service, bootstrap path, or
production image. Run its unit tests only as research:

```bash
GOCACHE=/tmp/probe-go-build-cache go test ./...
```
