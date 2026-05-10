# VPS Gap Analysis — Session 2026-05-09 Findings

## Environment
- **VPS:** Hostinger srv1651876.hstgr.cloud (8GB RAM, 2 CPU, 96GB disk)
- **Date:** 2026-05-09
- **Containers:** hermes-flux, openclaw, hermes-webui, flux-traefik, paperclip

## Gaps Found (by severity)

### 🔴 CRITICAL

#### Gap 1: ZERO Swap — OOM Kill Risk
- 7.7GB RAM, **0B swap** — confirmed with `free -h` and `swapon --show`
- All 5 containers have `memory=0` (no limits) — any can consume all RAM
- Hermes alone uses 1.76GB (22%) with no cap
- Paperclip already has RestartCount=1 (likely OOM)
- **Fix:** Create 4GB swap + set per-container limits (Hermes 3GB, OpenClaw 2GB, Paperclip 1GB, WebUI 512MB)

#### Gap 2: OpenClaw Outdated (v2026.4.21 vs v2026.5.7)
- Image from 2026-04-22, latest release is v2026.5.7
- `checkOnStart: false` in openclaw.json — won't auto-check updates
- **Fix:** Update image, set `checkOnStart: true`

#### Gap 3: No Container Memory/CPU Limits
- All containers: `memory=0, cpus=0`
- Under load, any container can starve others
- **Fix:** Add `--memory` and `--cpus` flags to each container

### 🟡 HIGH

#### Gap 4: Vision Provider Not Configured in Hermes
- Error: `No LLM provider configured for task=vision provider=auto`
- DeepSeek models don't support `image_url` → BadRequest errors
- **Fix:** Configure a vision-capable model (e.g., OpenAI GPT-5.4) for vision tasks

#### Gap 5: DNS Failures in OpenClaw
- `getaddrinfo ENOTFOUND api.nousresearch.com` — Ollama Cloud endpoint DNS unresolvable
- Failover to opencode-go/kimi-k2.6 works but adds ~26s delay
- Both deepseek-v4-pro and glm-5.1 fail before fallback succeeds
- **Fix:** Add public DNS (8.8.8.8/8.8.4.4) to container DNS config, or check Ollama Cloud endpoint URL

#### Gap 6: OpenClaw Plugins Failing Validation
- 5 plugins fail: `acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft`
- Validation errors on startup
- **Fix:** Remove unused plugins or fix their configuration

#### Gap 7: 8.91GB Dangling Docker Image
- `<none>:<none>` image occupying 8.91GB
- Total reclaimable: 12.9GB (48% of image storage)
- **Fix:** `docker image prune -a -f` (review first)

### 🟠 MEDIUM

#### Gap 8: Hardcoded WebUI Password in docker-compose.yml
- `HERMES_WEBUI_PASSWORD=FluxIA2026` in plaintext
- Also in commented docker-run command
- **Fix:** Use Docker secrets, `.env` file with restricted permissions, or secret management

#### Gap 9: Zero Backup Configuration
- No crontabs, no systemd timers
- Critical volumes: `paperclip-tjjz_data`, `/docker/hermes-agent-84im/data`
- No automated backup of configs, databases, or persistent data
- **Fix:** Set up daily backup cron for volumes and critical config files

#### Gap 10: Paperclip Restart
- RestartCount=1, started 2026-05-09T13:07
- Likely OOM-related given zero memory limits
- **Fix:** Apply memory limit, monitor logs

#### Gap 11: Unused Image (aionui:v1.9.25, 1.94GB)
- No active container using it
- **Fix:** Remove if no longer needed

### 🟢 LOW

#### Gap 12: Disk Usage 38%
- 36GB/96GB used — comfortable but growing
- Monitor Docker image accumulation

#### Gap 13: Hermes providers: {} in config.yaml
- Empty providers and fallback_providers
- Works via Ollama Cloud magic but no explicit fallback chain
- **Fix:** Define explicit fallback providers

## Diagnostic Commands Used

```bash
# System resources
free -h && swapon --show && uptime && df -h /

# Docker inventory + stats
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}'

# Container limits & restarts
docker inspect --format '{{.Name}}: restart={{.HostConfig.RestartPolicy.Name}}, memory={{.HostConfig.Memory}}, cpus={{.HostConfig.NanoCpus}}' $(docker ps -aq)

# DNS errors in OpenClaw
docker logs openclaw-4vbk-openclaw-1 2>&1 | grep -i "ENOTFOUND\|DNS lookup"

# Vision errors in Hermes
docker logs hermes-flux 2>&1 | grep -i "vision.*provider\|No LLM provider configured for task=vision"

# Reclaimable space
docker system df
docker images -f "dangling=true" --format 'table {{.ID}}\t{{.Size}}\t{{.CreatedAt}}'
```

## Priority Fix Order

1. ⚡ Create swap (4GB) — prevents OOM cascade
2. ⚡ Set container memory limits — prevents resource starvation
3. ⚡ Update OpenClaw image — security + features
4. 🔧 Fix DNS/vision/plugins — functionality
5. 🔧 Set up backups — data protection
6. 🧹 Clean dangling images — disk space