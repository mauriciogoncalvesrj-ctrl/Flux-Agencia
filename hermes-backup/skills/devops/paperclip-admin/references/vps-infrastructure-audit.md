# VPS Infrastructure Audit — Paperclip + Hermes + OpenClaw

## Audit Date: 2026-05-09

## Host Environment
- **Host:** Hostinger VPS (srv1651876.hstgr.cloud)
- **Resources:** 8GB RAM + 4GB swap, 96GB disk
- **Containers:** hermes-flux, paperclip-tjjz, openclaw-4vbk, flux-traefik, hermes-webui

## Critical Findings & Fixes Applied

### 1. Zero Swap → OOM Risk (FIXED)
- Created 4GB swap file at `/swapfile`, persisted in `/etc/fstab`
- **Pitfall:** Docker containers with no memory limits can consume all RAM, triggering OOM killer

### 2. No Memory Limits on Containers (FIXED)
- Applied via `docker update`:
  - hermes-flux: 3GB, openclaw: 2GB, paperclip: 1GB, webui: 512MB, traefik: 256MB
- **Pitfall:** `docker update --memory` only applies until container recreation. Hostinger "Atualizar" button recreates containers, losing limits.

### 3. OpenClaw DNS Failure (FIXED)
- `api.nousresearch.com` domain is dead (ENOTFOUND) — appears to have been retired
- Changed `baseUrl` in openclaw.json to `opencode.ai/zen/go/v1`
- Also disabled 5 broken plugins: acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft
- **Pitfall:** OpenClaw shows "warning" but still starts — check logs for ENOTFOUND

### 4. Paperclip Auth 401 Errors (FIXED)
- 126+ 401 errors caused by `PAPERCLIP_PUBLIC_URL=http://paperclip-tjjz.srv1651876.hstgr.cloud` vs actual domain `paperclip.somosflux.com.br`
- Patched `skipOriginCheck: true` in Better Auth (temporary — lost on container recreation)
- Reset admin password via PostgreSQL (scrypt hash) — env var `ADMIN_PASSWORD` only works on first bootstrap
- **Proper fix:** Recreate container with correct `PAPERCLIP_PUBLIC_URL` and `PAPERCLIP_ALLOWED_HOSTNAMES`

### 5. Docker Image Cleanup (FIXED)
- Removed 8.91GB dangling image and 1.94GB unused `aionui:v1.9.25`
- Total recovered: ~10.85GB

### 6. Hermes CLI Inside Paperclip (FIXED)
- CTO agent showed `status: error` with `adapterType: process` and `lastError: Process adapter missing command`
- Installed Python3, pip, copied Hermes venv + modules, symlinked CLI
- Changed adapter from `process` back to `hermes_local` via PATCH API
- **Pitfall:** `docker cp` preserves host UID/GID — must `chown` files inside container

### 7. Hermes Agent Config Gaps (FIXED)
- `providers: {}` → Added opencode-go provider with API key
- `fallback_providers: []` → Added glm-5.1 and kimi-k2.6 as fallbacks
- `checkpoints.enabled: false` → Changed to `true`
- `delegation.max_spawn_depth: 1` → Changed to `2`
- Vision provider: configured `opencode-go/glm-5.1` (supports text+image input)

### 8. Agent Model Standardization
Strategy for assigning models by role complexity:
- **deepseek-v4-pro** → CEO, CFO, CTO, dir-ghl (decisions, complex reasoning)
- **glm-5.1** → CMO, operations-director (operational tasks, cheaper)
- **kimi-k2.6** → sales-director (reasoning for sales qualification)

Model assignment via PATCH `/api/agents/:id?companyId=:companyId` with full `adapterConfig` object.

### 9. Backup Automation (CREATED)
- Cron job `flux-vps-backup` runs at 03:00 UTC daily
- Backs up: Paperclip PostgreSQL dump, Hermes config+env, OpenClaw config, container specs
- Retention: 7 days, stored in `/opt/data/backups/`
- Script at `/opt/data/cron/scripts/backup-vps.sh`

## Paperclip Agent Roster (Post-Fix)

| Agent | Model | Status | Heartbeat |
|-------|-------|--------|-----------|
| CEO | deepseek-v4-pro | idle | ✅ |
| CFO | deepseek-v4-pro | idle | ✅ |
| CTO | deepseek-v4-pro | idle | ✅ |
| CMO | glm-5.1 | idle | ✅ |
| dir-ghl | deepseek-v4-pro | idle | ❌ |
| operations-director | glm-5.1 | idle | ✅ |
| sales-director | kimi-k2.6 | idle | ✅ |
| test | deepseek-v4-flash | idle | ❌ |

## OpenClaw Provider Config (Post-Fix)

```json
{
  "ollama": {
    "baseUrl": "https://opencode.ai/zen/go/v1"
  }
}
```

Disabled plugins: acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft

## Pending Items
- [ ] Recreate Paperclip container with correct env vars (PAPERCLIP_PUBLIC_URL)
- [ ] Paperclip origin bypass patch will be lost on container recreation
- [ ] dir-ghl agent heartbeat not enabled
- [ ] test agent cleanup (or purpose unknown)