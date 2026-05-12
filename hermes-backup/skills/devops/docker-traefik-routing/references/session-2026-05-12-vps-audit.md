# VPS Infrastructure Audit — 2026-05-12

**Date:** 2026-05-12 ~01:38 UTC
**Performed by:** Hermes Agent (kimi-k2.6)
**Scope:** Hostinger VPS — full system scan (resources, Docker, Traefik, DNS, services)

---

## Executive Summary

7 active containers running. 7 distinct problem areas found. No OOM/critical resource exhaustion at audit time, but several ticking time bombs.

---

## 1. System Resources ✅

- **RAM:** 7.7 GB total, 2.9 GB used, 4.9 GB available — healthy
- **Swap:** 4.0 GB total, 443 MB used, 3.6 GB free — swap exists and is active
- **Disk:** 96 GB total, 65 GB used, 32 GB free (68%) — monitor for growth
- **Load:** 0.08 — virtually idle

**Verdict:** No critical resource pressure. Memory limits set on all containers are holding.

---

## 2. Docker Containers Status ✅ (but watch OpenClaw)

| Container | Status | Memory | CPU | Issue |
|-----------|--------|--------|-----|-------|
| `camofox-browser` | Up 34m (healthy) | 100 MB / 512 MB | 0.04% | OK |
| `open-design` | Up 2 days | 44 MB / 512 MB | 0.00% | OK |
| `hermes-webui` | Up 2 days (healthy) | 274 MB / 512 MB | 0.04% | OK |
| `openclaw-4vbk-openclaw-1` | Up 2 days | 1.59 GB / 2 GB | 0.33% | ⚠️ 80+ zombies |
| `hermes-flux` | Up 16m | 573 MB / 3 GB | 0.64% | ⚠️ session compressed 27x |
| `flux-traefik` | Up 3 days | 23 MB / 256 MB | 0.00% | ⚠️ NXDOMAIN errors |
| `paperclip-tjjz-paperclip-1` | Up 2 days | 450 MB / 1 GB | 0.02% | ⚠️ 401 loop |

**OpenClaw zombie crisis:** 80+ `<defunct>` processes (chromium, chrome-headless, chrome_crashpad, esbuild, ruby, pkill, MainThread, git, electron, curl). The container has been accumulating un-reaped child processes since May 9. Memory at 1.59 GB / 2 GB limit → approaching pressure.

**Hermes session compression:** 27 context compressions during this single session. Indicates extremely long context windows or poor model token efficiency. `Consider /new to start fresh` was printed 27 times.

---

## 3. Traefik Routing & SSL ❌

### Router/Service Label Audit

```bash
docker inspect --format='{{.Name}}: {{range $k,$v := .Config.Labels}}{{$k}}={{$v}} {{end}}' \
  $(docker ps -q) | grep "traefik\."
```

**Found:**
- `hermes-flux` → `certresolver=letsencrypt` ✅
- `open-design` → `certresolver=letsencrypt` ✅
- `paperclip-tjjz-paperclip-1` → `certresolver=letsencrypt` ✅
- `camofox-browser` → `certresolver=letsencrypt` ✅
- `openclaw-4vbk-openclaw-1` → `certresolver=default` ⚠️ — **MISMATCH!**
- `hermes-webui` → `certresolver=letsencrypt` ✅

**Impact:** OpenClaw's router references `default` resolver, but Traefik only has `letsencrypt.acme` or `letsencrypt`. This may cause OpenClaw's SSL certificate to fail or fall back to a default (self-signed) cert.

### NXDOMAIN Errors in Traefik Logs

Traefik repeatedly fails Let's Encrypt validation for:
- `design.somosflux.com.br` — DNS record does not exist
- `aion.somosflux.com.br` — DNS record does not exist
- `camofox.somosflux.com.br` — DNS record does not exist

Full error:
```
acme: error: 400 :: urn:ietf:params:acme:error:dns ::
DNS problem: NXDOMAIN looking up A for design.somosflux.com.br
```

**Verdict:** These subdomains are configured in Traefik routes but have no A records in DNS. Let's Encrypt cannot issue certs for non-resolvable domains. Traefik will retry indefinitely.

### File Provider Config (`/letsencrypt/somosflux.yml`)

Routes defined:
- `hermes-somosflux` → `http://hermes-flux:9119` ✅
- `openclaw-somosflux` → `http://openclaw-4vbk-openclaw-1:64551` ✅
- `paperclip-somosflux` → `http://paperclip-tjjz-paperclip-1:3100` ✅
- `aionui-somosflux` → `http://aionui:25808` ⚠️ — container `aionui` does not exist

**Impact:** `aion.somosflux.com.br` route points to a non-existent container. Returns 502 or connection refused.

### Subdomain Reachability Test

```bash
for sub in design hub paperclip openclaw; do
  curl -sI --connect-timeout 3 "https://$sub.somosflux.com.br" | head -1
done
```

| Subdomain | Result |
|-----------|--------|
| `design.somosflux.com.br` | FAIL (DNS resolution fails — NXDOMAIN) |
| `hub.somosflux.com.br` | HTTP/2 401 ✅ (expected — basic auth) |
| `paperclip.somosflux.com.br` | HTTP/2 200 ✅ |
| `openclaw.somosflux.com.br` | HTTP/2 200 ✅ |

---

## 4. Service Health

### Hermes Gateway Port 8642

```bash
curl -s http://127.0.0.1:8642/health  # → 000, 0.000s
```

**Port bindings exist:**
```
8642/tcp → 0.0.0.0:8642
8642/tcp → [::]:8642
9119/tcp → 0.0.0.0:9119
9119/tcp → [::]:9119
```

**But process not listening internally:**
```bash
docker exec hermes-flux sh -c "cat /proc/net/tcp | grep -i $(printf '%04X' 8642)"
# No output
```

**Verdict:** Port 8642 is published by Docker but the Hermes process is not binding to it. Only port 9119 (dashboard) is active. Port 8642 may be for an alternate gateway mode that is not running.

### Paperclip 401 Loop

Paperclip logs show a **5-minute periodic** pattern:
```
20:51:03 WARN GET /api/companies/.../issues?assigneeAgentId=... 401
20:51:03 WARN GET /api/companies/.../issues?status=backlog 401
20:56:34 WARN GET /api/companies/.../issues?assigneeAgentId=... 401
```

**Same endpoints WITHOUT `/api/` prefix return 200:**
```
20:52:17 INFO GET /companies/.../issues 200
```

**Root cause hypothesis:** A Paperclip agent (OpenClaw integration or heartbeat cron) is calling the REST API with an invalid/mismatched origin or expired session token. The `/api/` prefix enforces auth; root-level paths don't.

**Agent ID involved:** `763e73f1-326c-4ba1-8c72-2b860a26e4c1`

### n8n — OFFLINE

`n8n` container does not exist in `docker ps -a`. Service is completely down.

### Google Ads MCP — OFFLINE

No `google-ads-mcp` process or container found. File `/opt/data/google-ads-adc.json` exists with credentials but no service is running.

### OpenClaw — Functional but Unstable

- Main process: `node server.mjs` (PID 9) running
- OpenClaw binary: `openclaw` (PID 22, 696 MB RSS)
- **80+ zombie processes** accumulated over 3 days
- Memory at 1.59 GB / 2 GB limit

### Hermes MCP Servers — All Running ✅

| MCP Server | Status |
|------------|--------|
| `fal-mcp` | ✅ Running (balance: unknown) |
| `camofox-mcp@latest` | ✅ Running |
| `meta-ads-mcp` | ✅ Running |
| `ghl-mcp` | ✅ Running (Location Private Integration token known) |
| `google-ads-mcp` | ❌ Not running |

---

## 5. Security Notes

- `google-ads-adc.json` contains refresh token in plaintext at `/opt/data/` — review permissions (`-rw-r--r--`, world-readable inside container)
- No firewall (`ufw`) visible from inside container
- `0.0.0.0` bindings on multiple ports — expected for Docker, monitor for unnecessary exposure

---

## 6. Recommended Fixes (Priority Order)

### 🔴 URGENT

1. **Restart OpenClaw container** — clear 80+ zombie processes before they exhaust PID limit or trigger OOM
2. **Fix OpenClaw certresolver label** — change `certresolver=default` to `certresolver=letsencrypt`
3. **Add DNS A records** for `design.somosflux.com.br`, `aion.somosflux.com.br`, `camofox.somosflux.com.br`

### 🟡 HIGH

4. **Fix Paperclip 401 loop** — identify and update the integration (likely OpenClaw agent) calling `/api/` with invalid auth
5. **Recreate n8n container** if still needed
6. **Restart Google Ads MCP** using credentials from `/opt/data/google-ads-adc.json`

### 🟢 LOW

7. **Investigate Hermes port 8642** — verify if Gateway should be running on this port or if it's deprecated
8. **Clean OpenClaw disk** — remove dangling images (check with `docker system df`)

---

## Commands Used (Reusable)

### Full container label dump
```bash
docker inspect --format='{{.Name}}: {{range $k,$v := .Config.Labels}}{{$k}}={{$v}} {{end}}' \
  $(docker ps -q) | grep "traefik\."
```

### Check Traefik file provider config
```bash
docker exec flux-traefik cat /letsencrypt/somosflux.yml
```

### Check ACME certificates
```bash
docker exec flux-traefik sh -c "cat /letsencrypt/acme.json | grep -o '\"San\":\[.*\]'" | head -10
```

### Check DNS via curl (no dig needed)
```bash
for sub in design hub paperclip openclaw; do
  echo -n "$sub.somosflux.com.br: "
  curl -sI --connect-timeout 3 "https://$sub.somosflux.com.br" | head -1
done
```

### Count zombies per container
```bash
for c in $(docker ps -q); do
  count=$(docker exec "$c" ps aux 2>/dev/null | grep -c defunct || echo 0)
  [ "$count" -gt 0 ] && echo "$(docker inspect --format '{{.Name}}' $c): $count zombies"
done
```

### Check if port is actually listening inside container
```bash
docker exec <container> sh -c "cat /proc/net/tcp | grep -i $(printf '%04X' <port>)"
```

---

## Follow-Up

User asked to "analyze deeply, I think we have many problems, check logs and fix everything." This audit document was generated. The user was presented with a summary of 7 problems and asked for explicit approval (`"inicia"`) before applying fixes.
