# Session 2026-05-08: File Provider Fix for Hostinger VPS

## Problem
User had 4 Docker services on a Hostinger VPS managed via panel:
- Hermes Agent, OpenClaw, Paperclip, Traefik

All were on the shared `proxy` network, but their Traefik labels only pointed to `srv1651876.hstgr.cloud` subdomains. User added DNS A records for `*.somosflux.com.br` pointing to the VPS, but accessing those domains returned **Gateway Timeout**.

## Root Cause
The `hermes-flux` container was connected to `proxy` network, but the Traefik router label `hermes-agent-84im` pointed to `http://172.16.1.2:9119` (the IP on the OTHER network `hermes-agent-84im_default`). When we connected `hermes-flux` to `proxy`, it got a new IP `172.18.0.3`, but the old router still tried `172.16.1.2` — hence Gateway Timeout.

Wait, actually the real root cause for the 404s when we first tested `somosflux.com.br` was simply that there were **no routers configured for those domains at all**.

## Solution Evolution

### Phase 1: Router Container (quick fix)
Created `somosflux-router` (busybox) on `proxy` network with labels for all 3 domains.
Hit pitfall: `ERR Router X cannot be linked automatically with multiple Services` — fixed by adding explicit `traefik.http.routers.<name>.service=<svc>`.

Tested OK:
- `hermes.somosflux.com.br` → 200
- `openclaw.somosflux.com.br` → 200
- `paperclip.somosflux.com.br` → 200

### Phase 2: File Provider (definitive fix)
User explicitly asked: *"qual seria a melhor forma de resolver isso logo, e não esperar dar problemas, pois tbm uso muito o botão de atualizar na vps."*

Since the user updates via Hostinger panel button, the router container would be lost on recreation.

**Created** `/letsencrypt/somosflux.yml` inside the Traefik container. The `/letsencrypt` directory is a host bind-mount (`/opt/flux-stack/traefik/letsencrypt`), so it persists across recreation.

**Pitfall encountered**: Writing the file via `docker exec ... sh -c` with double quotes caused backtick escaping issues in YAML:
```
ERR Error while building configuration: yaml: line 4: found unknown escape character
```

**Fix**: Use a heredoc with single-quoted delimiter and single-quoted YAML strings:
```bash
docker exec traefik sh -c "cat > /letsencrypt/routes.yml << 'EOF'
http:
  routers:
    app:
      rule: 'Host(\`app.example.com\`)'
EOF"
```

**Restarted Traefik** with flags:
```
--providers.file.directory=/letsencrypt/
--providers.file.watch=true
```

**Removed** `somosflux-router` container.

All 3 domains still responding 200. The config file survives any future Traefik recreation as long as the volume mount and the `--providers.file.*` flags are present.

## Remaining Risk
If Hostinger's panel recreates Traefik and does NOT include `--providers.file.directory=/letsencrypt/` and `--providers.file.watch=true`, the file will exist but won't be read. The fix then is simply adding those two CLI flags to the Traefik service.

## Docker Cleanup Performed
Removed:
- `paperclip-tjjz-paperclip-1-old` (stopped, conflicting bind mount)
- `flux-paperclip` (stopped, old flux-stack paperclip)
- `ghcr.io/hostinger/hvps-hermes-agent:latest` image (9.84 GB, unused duplicate)
- `traefik/whoami:latest` image (11.3 MB, test image)
- 2 dangling images (17.7 GB total)
- 3 orphaned volumes
- 2 empty networks

Total freed: ~27 GB.

## Network Map (final)
| Container | Networks | IP on proxy |
|---|---|---|
| hermes-flux | hermes-agent-84im_default, proxy | 172.18.0.3 |
| openclaw-4vbk-openclaw-1 | hermes-net, proxy | 172.18.0.5 |
| paperclip-tjjz-paperclip-1 | hermes-net, proxy | 172.18.0.7 |
| flux-traefik | proxy | 172.18.0.2 |
