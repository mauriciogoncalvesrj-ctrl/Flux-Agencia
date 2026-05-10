# Session Reference: Network Reconnect Fix (2026-05-08)

## Context

Hostinger VPS with Docker Compose Catalog. Services managed via Hostinger panel:
- `hermes-flux` (Hermes Agent) — port 9119 (dashboard)
- `openclaw-4vbk-openclaw-1` (OpenClaw) — port 64551
- `paperclip-tjjz-paperclip-1` (Paperclip) — port 3100
- `flux-traefik` (Traefik reverse proxy) — ports 80/443

Custom domains pointing to VPS: `hermes.somosflux.com.br`, `openclaw.somosflux.com.br`, `paperclip.somosflux.com.br`

## Problem

`https://hermes.somosflux.com.br/` returned **502 Bad Gateway**.

Root cause: In a previous session, `docker network connect proxy hermes-flux` was run manually to fix a cross-network issue. The Hostinger panel later recreated the `hermes-flux` container (likely via the "Atualizar" button), which erased the runtime network attachment. The container reverted to its original network `hermes-agent-84im_default`, isolating it from Traefik's `proxy` network.

## Diagnosis Steps

```bash
# Confirmed 502 from outside
curl -s -o /dev/null -w "%{http_code}" https://hermes.somosflux.com.br/   # -> 502

# Checked container networks
docker inspect hermes-flux --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
# -> hermes-agent-84im_default   (MISSING: proxy)

docker inspect flux-traefik --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
# -> proxy

# Other services were unaffected — they were already on both networks:
# openclaw-4vbk-openclaw-1: hermes-net proxy
# paperclip-tjjz-paperclip-1: hermes-net proxy
```

## Immediate Fix

```bash
docker network connect proxy hermes-flux
```

Verification:
```bash
docker run --rm --network proxy busybox wget -qO- --timeout=5 http://hermes-flux:9119/
# -> HTML response (200)

curl -s -o /dev/null -w "%{http_code}" https://hermes.somosflux.com.br/
# -> 200 (0.013s)
```

## Permanent Fix: Automated Monitoring

Created `/opt/data/scripts/fix-traefik-network.sh` (specific instance of the generic `scripts/network-monitor.sh` template). Key configuration for this environment:

```bash
TRAEFIK_NETWORK="proxy"
SERVICES="hermes-flux:9119,openclaw-4vbk-openclaw-1:64551,paperclip-tjjz-paperclip-1:3100"
LOG_FILE="/opt/data/logs/network-fix.log"
```

Scheduled via cron with `no_agent: true` (plain shell execution, no LLM inference):
- Name: `traefik-network-fix`
- Schedule: `every 5m`
- Script: `fix-traefik-network.sh`

The script logs to `/opt/data/logs/network-fix.log` and handles:
1. Detecting missing network attachments
2. Auto-reconnecting containers
3. Health-checking via the proxy network

## Key Insight

Runtime Docker network attachments (`docker network connect`) are **not** persisted across container recreation by managed panels. The Traefik File Provider (`/letsencrypt/somosflux.yml`) persists routing rules, but it does NOT persist network membership. Both layers need protection:
- **Routing**: File Provider YAML on host-mounted volume
- **Network membership**: Monitoring script that repairs runtime state

## Files Created

- `/opt/data/scripts/fix-traefik-network.sh` — environment-specific monitor
- `/opt/data/logs/network-fix.log` — audit trail

## Follow-up Risk

If the Hostinger panel recreates the Traefik container itself (not just the app containers), the `--providers.file.directory=/letsencrypt/` flag could be lost. The YAML file would still exist on disk but Traefik would not read it. This requires recreating Traefik with the file provider flags (see main SKILL.md for the full docker run command).
