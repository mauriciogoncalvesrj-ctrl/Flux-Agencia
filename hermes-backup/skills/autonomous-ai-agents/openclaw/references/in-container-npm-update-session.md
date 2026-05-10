# OpenClaw In-Container npm Update — Session Notes

## Context
Hostinger VPS Docker Compose deployment. The Docker image (`ghcr.io/hostinger/hvps-openclaw:latest`) was 16 days stale (2026.4.21) while npm already had 2026.5.7.

## Discovery
- `docker pull ghcr.io/hostinger/hvps-openclaw:latest` returned "Status: Image is up to date" even though GitHub showed a newer release.
- Hostinger panel "Atualizar" would recreate from the same stale image.
- Inside the container, `openclaw update` exists and can install a newer npm build into `/data/.npm-global/lib/node_modules/openclaw`.

## Execution Flow Inside Container

```
Docker image layer (root):  /usr/local/bin/openclaw  →  /usr/local/lib/node_modules/openclaw/openclaw.mjs
                              (old version from image, read-only)

npm update writes to:        /data/.npm-global/bin/openclaw
                              (new version, persisted in data volume)

PATH order for node user:    /data/.npm-global/bin  BEFORE  /usr/local/bin
```

The `entrypoint.sh` runs as root and does `chown -R node:node /data`, then drops to the `node` user with `runuser -u node -- node server.mjs`.

## Key Commands Used

```bash
# Check current version
docker exec openclaw-4vbk-openclaw-1 openclaw --version

# Check update availability
docker exec openclaw-4vbk-openclaw-1 openclaw update status --json

# Dry-run preview
docker exec openclaw-4vbk-openclaw-1 openclaw update --dry-run --json --yes

# Apply update (no gateway restart, just CLI install)
docker exec openclaw-4vbk-openclaw-1 openclaw update --yes --no-restart --json

# Must restart container after npm update
# If you only restart the gateway process, the old binary remains in effect
docker restart openclaw-4vbk-openclaw-1

# Verify after restart
docker exec openclaw-4vbk-openclaw-1 openclaw --version
docker exec openclaw-4vbk-openclaw-1 openclaw health
```

## Verification Output (Good)

```
OpenClaw 2026.5.7 (eeef486)

Gateway event loop: degraded reasons=event_loop_utilization,cpu
Agents: main (default)
Session store (main): /data/.openclaw/agents/main/sessions/sessions.json (1 entries)
```

## Anti-Pattern to Avoid

Running `openclaw update --no-restart` and then only restarting the gateway process (e.g., `openclaw gateway run`) does NOT pick up the new binary because the old `openclaw` binary from `/usr/local/bin/` is still the first `PATH` entry in the running shell. A full Docker container restart is required.

## Summary

| Method | Image Layer | CLI Binary | Gateway Process | Works When |
|--------|------------|-----------|----------------|------------|
| Panel "Atualizar" | Refreshed | Refreshed | Refreshed | New image published |
| `docker pull` + restart | Updated | Updated | Updated | Image exists in registry |
| `openclaw update --yes` | Stays old | Updated in data volume | Stays old | Immediate CLI upgrade |
| `openclaw update` + container restart | Stays old | Updated in data volume | Updated | Immediate full upgrade |

The container-restart method is the best workaround when Hostinger's image is delayed.
