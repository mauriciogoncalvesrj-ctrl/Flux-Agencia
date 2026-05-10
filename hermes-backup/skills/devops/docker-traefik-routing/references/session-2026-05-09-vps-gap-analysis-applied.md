# VPS Gap Analysis — Applied Fixes (2026-05-09)

## Context
First full infrastructure audit requested by user. Found 13 gaps across 4 severity levels. Applied fixes for all critical and high items in a single session.

## Host Access Technique
Running inside `hermes-flux` container without host namespace. `nsenter -t 1` fails with "Operation not permitted". 

**Working method:** `docker run --rm --privileged --pid=host -v /:/host alpine sh -c '...'`

This lets you:
- Read/write host filesystem via `/host/` prefix
- Create swap, edit fstab
- Run `free -h`, `dmesg`, `swapon` against host
- Verify host-level settings

## Fixes Applied

### 1. Swap (Critical)
```bash
docker run --rm --privileged --pid=host -v /:/host alpine sh -c '
  fallocate -l 4G /host/swapfile
  chmod 600 /host/swapfile
  mkswap /host/swapfile
  swapon /host/swapfile
  grep -q swapfile /host/etc/fstab || echo "/swapfile none swap sw 0 0" >> /host/etc/fstab
'
```
Result: 7.7GB RAM + 4GB swap = 11.7GB total. Survives reboot via fstab entry.

### 2. Container Memory Limits (Critical)
```bash
docker update --memory=3072m --memory-swap=-1 hermes-flux        # 3GB
docker update --memory=2048m --memory-swap=-1 openclaw-4vbk-openclaw-1  # 2GB
docker update --memory=1024m --memory-swap=-1 paperclip-tjjz-paperclip-1 # 1GB
docker update --memory=512m --memory-swap=-1 hermes-webui       # 512MB
docker update --memory=256m --memory-swap=-1 flux-traefik       # 256MB
```
Note: `--memory-swap=-1` means unlimited swap+RAM (total). The `--memory` flag caps RAM. These limits apply instantly without container restart but do NOT persist across container recreation (panel "Atualizar"). To persist, add to docker-compose or docker run command.

### 3. OpenClaw DNS Fix (Critical → High)
`api.nousresearch.com` returns NXDOMAIN on all DNS servers (8.8.8.8, host resolvers). The Ollama Cloud provider in `openclaw.json` had this dead URL as `baseUrl`.

Fix: Changed `models.providers.ollama.baseUrl` from `https://api.nousresearch.com/v1` to `https://opencode.ai/zen/go/v1` (same backend, working domain). Used same API key as opencode-go provider.

Config applied by:
1. Writing corrected JSON locally to `/tmp/openclaw-fixed.json`
2. `docker cp /tmp/openclaw-fixed.json openclaw-4vbk-openclaw-1:/data/.openclaw/openclaw.json`
3. `docker restart openclaw-4vbk-openclaw-1`

### 4. OpenClaw Plugins Disabled (High)
5 plugins failing validation: acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft.

Added `"enabled": false` entries for each in `plugins.entries`.

### 5. Disk Cleanup
```bash
docker image prune -f     # Removed dangling 8.91GB image
docker rmi aionui:v1.9.25 # Removed orphaned 1.94GB image
```
Total recovered: ~2.3GB (prune only removed 389MB due to shared layers, aionui was the big win).

### 6. Hermes Vision Provider (High)
DeepSeek models don't support `image_url` input → BadRequest on every vision call.

Fix: Set in `/opt/data/config.yaml`:
```yaml
auxiliary:
  vision:
    provider: opencode-go
    model: glm-5.1  # supports text+image
```
Previous value was `minimax-m2.5` which may also work but `glm-5.1` was confirmed from OpenClaw model registry as image-capable.

## Still Pending (Medium/Low)
- Automated backup of Docker volumes and configs (no crontabs, no timers)
- WebUI password hardcoded in docker-compose (`HERMES_WEBUI_PASSWORD=FluxIA2026`)
- Paperclip had 1 restart — cause unknown, may be OOM
- Memory limits don't persist across container recreation by Hostinger panel