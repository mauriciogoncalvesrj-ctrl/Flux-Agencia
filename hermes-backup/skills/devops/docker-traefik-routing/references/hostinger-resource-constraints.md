# Hostinger VPS — Resource Constraints & OOM Diagnosis

## Critical Finding: NO SWAP

Hostinger VPS deployments ship with **zero swap space**. This is the #1 cause of intermittent service outages.

### How to verify (when Docker is unavailable)
```bash
cat /proc/meminfo | grep -E "^(MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree)"
```
If `SwapTotal: 0 kB`, the VPS has no swap. When RAM fills, the Linux OOM Killer terminates processes.

### The OOM Cascade
1. Multiple AI services consume RAM (Hermes 2-4GB, OpenClaw 1-3GB, Paperclip 1GB, PostgreSQL ~1GB)
2. Any service with `restart: unless-stopped` auto-restarts after OOM kill
3. Restarted services reload models/reconnect, causing another RAM spike
4. Cycle repeats — services flapping, user loses access intermittently

### Fix: Create Swap File
```bash
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```
4GB of swap prevents 90% of OOM-related outages.

### Fix: Container Memory Limits
Set explicit limits to prevent one service from consuming all RAM:
- Hermes Agent: `--memory=3g`
- OpenClaw: `--memory=2g`
- Paperclip: `--memory=1g`

This ensures no single container can starve the others.

## Diagnostic Methodology When Docker Socket is Unavailable

When the Hermes container doesn't have `/var/run/docker.sock` mounted, use these alternatives:

### 1. System Memory (no Docker needed)
```bash
cat /proc/meminfo | head -20   # RAM + swap status
cat /proc/cpuinfo | grep processor | wc -l   # CPU count
cat /proc/loadavg   # Load average
```

### 2. Service Health Checks via HTTP
```bash
curl -sk -w "\nHTTP:%{http_code}\n" --connect-timeout 10 https://openclaw.somosflux.com.br/
curl -sk -w "\nHTTP:%{http_code}\n" --connect-timeout 10 https://paperclip.somosflux.com.br/
curl -sk -w "\nHTTP:%{http_code}\n" --connect-timeout 10 https://hub.somosflux.com.br/
curl -sk -w "\nHTTP:%{http_code}\n" --connect-timeout 10 https://hermes.somosflux.com.br/
```
All responding = services are up. Timeouts/refused = containers down.

### 3. Gateway Log Analysis
```bash
# Check for gateway crashes
grep -i "exiting with code\|shutdown\|heartbeat\|fail" ~/.hermes/logs/gateway.log | tail -20

# Check for external API errors
grep -i "503\|overloaded\|timeout\|error" ~/.hermes/logs/errors.log | tail -20
```

**Key crash signature** (OOM or signal kill):
```
gateway.run: Exiting with code 1 (signal-initiated shutdown without restart request)
```
This means the process was killed externally — typically OOM Killer or Docker daemon restart.

### 4. Session History Search
Before diagnosing from scratch, search past sessions:
```bash
session_search --query "docker OR container OR restart OR OOM" --limit 5
```
Previous fixes may have been undone by Hostinger panel container recreation.

## All Services Currently UP Check (Quick Script)
```bash
for svc in "openclaw.somosflux.com.br" "paperclip.somosflux.com.br" "hub.somosflux.com.br" "hermes.somosflux.com.br"; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://$svc/")
  echo "$svc → HTTP $code"
done
```

## Known Environment Specs
- **VPS RAM:** 8GB
- **VPS CPUs:** 2
- **Disk:** ~96GB total, ~60GB available
- **Operating System:** Debian (Docker host)
- **Swap:** 0 (ZERO — critical vulnerability)
- **Docker socket:** NOT mounted in hermes-flux container by default (needs volume mount)

## OpenClaw DNS Resolution Failures (2026-05-09)

When OpenClaw containers cannot resolve provider endpoints, the error appears as:
```
getaddrinfo ENOTFOUND api.nousresearch.com
```

This causes all Ollama Cloud models (deepseek-v4-pro, glm-5.1, kimi-k2.6) to fail sequentially before fallback to opencode-go providers succeeds — adding ~26 seconds of latency per request.

### Root cause
Docker's internal DNS resolver (127.0.0.11) may fail to resolve external API hostnames if upstream DNS is unreliable or if the container's `/etc/resolv.conf` has malformed configuration.

### Fix
1. Verify current DNS inside the container:
   ```bash
   docker exec openclaw-4vbk-openclaw-1 cat /etc/resolv.conf
   ```
2. Add public DNS servers via Docker compose or docker run:
   ```yaml
   dns:
     - 8.8.8.8
     - 8.8.4.4
     - 1.1.1.1
   ```
3. Or add `--dns 8.8.8.8 --dns 8.8.4.4` to `docker run` commands.

## Hermes Vision Provider Failures (2026-05-09)

DeepSeek models routed through Ollama Cloud do NOT support the `image_url` content type, causing:
```
openai.BadRequestError: Error code: 400 - unknown variant `image_url`, expected `text`
```

Also seen as:
```
No LLM provider configured for task=vision provider=auto
```

### Fix
Configure a vision-capable model explicitly in Hermes config:
```bash
hermes config set model.vision.provider openai
hermes config set model.vision.model gpt-5.4
```
Or set in config.yaml under the vision task section.
