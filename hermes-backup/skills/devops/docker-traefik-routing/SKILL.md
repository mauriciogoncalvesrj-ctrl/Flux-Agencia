---
name: docker-traefik-routing
category: devops
description: Diagnose and fix Traefik reverse-proxy routing issues in Docker environments, especially cross-network connectivity, Gateway Timeout errors, and adding routes to existing managed containers without editing docker-compose files.
triggers:
  - Traefik returns 502 Bad Gateway or 504 Gateway Timeout
  - Container labels exist but route does not work
  - Need to expose an existing Docker service on a new domain
  - Docker containers on different networks cannot communicate
  - Hostinger / managed panel Docker Compose — can't edit compose files directly
  - Adding custom domains to services already exposed on random ports
related_skills:
  - paperclip-admin
---

# Docker Traefik Routing

## Pre-Diagnosis Checklist

Before running commands on a reported routing failure, check whether this is a **recurring issue** that was recently addressed. Managed panels (Hostinger, etc.) can recreate containers hours or days later, silently undoing previous fixes.

1. **Search session history** for recent work on the same domain or service:
   ```bash
   session_search --query "domain.com OR service-name"
   ```
   If the user says *"already done"* or *"it was working before"*, the root cause is almost certainly a **container recreation** that erased runtime state (network attachments, env vars, file provider flags).

2. **Verify current container state** rather than assuming the previous fix is still active:
   ```bash
   docker inspect <container> --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
   docker inspect <container> --format='{{json .Config.Labels}}'
   ```

3. **Confirm original access paths** are still working (panel links, direct ports). This narrows down whether the issue is Traefik-specific or a broader outage.

4. **Check for container recreation** by comparing `Created` time with the last known working time:
   ```bash
   docker inspect <container> --format='{{.State.StartedAt}}'
   ```

## Quick Diagnosis

1. **Check container networks:**
   ```bash
   docker inspect <container> --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} | {{$v.IPAddress}}\n{{end}}'
   ```
   If Traefik and the target are on different networks, Traefik cannot resolve the container name.

2. **Test connectivity from Traefik:**
   ```bash
   docker exec <traefik-container> wget -qO- --timeout=5 http://<target>:<port>/
   ```
   If this fails with "bad address", the networks are isolated.

3. **Check Traefik labels on target:**
   ```bash
   docker inspect <container> --format '{{json .Config.Labels}}'
   ```
   Verify `traefik.enable=true`, `traefik.docker.network=proxy`, and router/service labels.

## Fix: Connect Container to Shared Network

The fastest fix for cross-network issues:
```bash
docker network connect <shared-network> <container>
```

- Do NOT restart the container — this is hot-plug.
- Verify with `docker exec <traefik> wget ...` again.

## Fix: Add Routes Without Editing docker-compose

When compose files are managed by a panel (Hostinger, etc.) and can't be edited directly, you have two options. **Prefer the File Provider** for permanence.

### Option A (Definitive): Traefik File Provider

Create a YAML file in a directory that Traefik already mounts as a volume (e.g., `/letsencrypt/` or `/opt/flux-stack/traefik/`):

```yaml
# /letsencrypt/somosflux.yml
http:
  routers:
    myservice-somosflux:
      rule: 'Host(`myservice.example.com`)'
      entryPoints:
        - websecure
      service: myservice-somosflux
      tls:
        certResolver: letsencrypt

  services:
    myservice-somosflux:
      loadBalancer:
        servers:
          - url: 'http://<target-container>:<port>'
```

Then add the File Provider flag when starting Traefik:
```bash
--providers.file.directory=/letsencrypt/
--providers.file.watch=true
```

**Why this is better than a router container:**
- Survives container recreation — the YAML is on a host-mounted volume
- No extra "ghost" container running
- Works even if the Traefik container is rebuilt by the panel
- Only requirement: the directory must be mounted as a volume in the Traefik compose config

**Pitfall — YAML backtick escaping:**
When writing the file via `docker exec ... sh -c`, backticks in the `rule` field are interpreted by the shell. Write the file using a heredoc with **single-quoted delimiter** (`<< 'EOF'`) and single-quoted YAML strings:
```bash
docker exec traefik sh -c "cat > /letsencrypt/routes.yml << 'EOF'
http:
  routers:
    app:
      rule: 'Host(\`app.example.com\`)'
EOF"
```
Double quotes or unquoted backticks will cause: `yaml: line 4: found unknown escape character`.

### Option B (Quick): Router Container

For a fast temporary fix, create a container that holds only Traefik labels:

```bash
docker run -d --name <router-name> --network <traefik-network> \
  --restart unless-stopped \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=<traefik-network>" \
  -l "traefik.http.routers.<name>.entrypoints=websecure" \
  -l "traefik.http.routers.<name>.rule=Host(\`domain.com\`)" \
  -l "traefik.http.routers.<name>.tls.certresolver=letsencrypt" \
  -l "traefik.http.routers.<name>.service=<svc-name>" \
  -l "traefik.http.services.<svc-name>.loadbalancer.server.url=http://<target>:<port>" \
  busybox sleep infinity
```

### Critical Pitfall: Explicit Service Linkage

When a single container has **multiple Traefik services**, Traefik CANNOT auto-link routers to services. You **must** add:
```
traefik.http.routers.<name>.service=<svc-name>
```

Without this, Traefik logs:  
`ERR Router X cannot be linked automatically with multiple Services`

## Preserving Existing Access

When adding custom domains, the original port mappings (`0.0.0.0:PORT->CONTAINER_PORT`) and existing Traefik labels remain untouched. The router container only **adds** new routes — it does not replace or conflict with:
- Hostinger panel "Abrir" links
- Direct port access
- Existing `srvXXXX.hstgr.cloud` Traefik labels

## Self-Healing: Auto-Reconnect After Panel Recreation

**The problem:** Managed panels (Hostinger, etc.) that recreate containers via "Update" / "Atualizar" buttons rebuild containers from their original compose definitions. Any manual changes made at runtime — such as `docker network connect proxy <container>` — are lost. The container reverts to its original network list, breaking Traefik routing and producing 502 errors.

**The solution:** A lightweight monitoring script running inside a container that has access to `docker.sock`. It checks every few minutes whether critical containers are connected to the shared Traefik network, and reconnects them automatically if they are missing.

### Setup

1. Ensure the monitoring container (or the Hermes Agent container itself) has `docker.sock` mounted:
   ```yaml
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock:rw
   ```

2. Create the monitoring script (see `scripts/network-monitor.sh` for a generic template).

3. Schedule it via cron (inside the container) with `no_agent: true` so it runs as a plain shell script:
   ```
   every 5m -> scripts/network-monitor.sh
   ```

### What the script does

- Checks each critical service container's networks
- If a container is missing the Traefik network, runs `docker network connect <network> <container>`
- Performs a health check via the Traefik network (e.g., `wget http://target:port/`)
- Logs all actions to a file for auditability

### Key pitfall: Container recreation erases runtime state

`docker network connect` is a **runtime-only** change. It does NOT modify the underlying docker-compose file. When a managed panel recreates the container, the network attachment disappears. The only persistent solutions are:
- Editing the original docker-compose (not possible with Hostinger panel)
- Using the Traefik File Provider (persists across Traefik restarts, but does not fix network detachment)
- The monitoring script (catches and repairs the detachment automatically)

All three approaches can be used together: File Provider for routing permanence, and the monitor script for network resilience.

## Pitfall: Application-Level Network Bind (e.g., OpenClaw gateway)

Some services have their OWN network binding logic — not just Docker port mapping. Even if the container is on the correct network with the correct port exposure, the **application inside** may bind only to `127.0.0.1` (loopback), refusing connections from the Docker bridge network.

**Symptom:**
- `docker exec traefik wget http://target:64551/` → **Connection refused**
- Container is on `proxy` network
- Port mapping exists (`-p 64551:64551`)
- Traefik still gets **504** or **connection refused**

**Root cause:** The application's own config has `bind: loopback` or `127.0.0.1` in its internal server config. Examples:
- OpenClaw: `gateway.bind` field in `openclaw.json`
- Node.js: `server.listen(port, '127.0.0.1')`
- Python Flask: `app.run(host='127.0.0.1')`

**Diagnosis:**
```bash
# Check what the application is actually listening on INSIDE the container
docker exec <container> ss -tlnp
docker exec <container> netstat -tlnp
# If you see 127.0.0.1:PORT instead of 0.0.0.0:PORT, it's a loopback bind
```

**Fix:**
Edit the application's own configuration to bind to all interfaces. For OpenClaw:
```json
"gateway": {
  "bind": "lan",
  "port": 64551
}
```
This is the OpenClaw-specific `lan` value meaning `0.0.0.0`. Other applications may use `0.0.0.0`, `*`, `::`, or a config key like `host: 0.0.0.0`, `bind: 0.0.0.0`, or `listen: all`.

**Key lesson:** Docker network + Traefik labels only solve half the problem. The application itself must listen on an address reachable from the Docker bridge network (`172.x.x.x`). If the app is only on `127.0.0.1`, Traefik cannot reach it even though it's in the same Docker network.

---

## Diagnostic: Dumping All Traefik Labels Across Containers

When auditing a live VPS, quickly check ALL Traefik labels in one shot:
```bash
docker inspect --format='{{.Name}}: {{range $k,$v := .Config.Labels}}{{$k}}={{$v}} {{end}}' \
  $(docker ps -q) | grep "traefik\." | sed 's/ traefik\./\n  traefik./g'
```

Use this to detect:
- **certresolver mismatches** — one container uses `certresolver=default`, another uses `certresolver=letsencrypt` — whichever Traefik doesn't have configured will fail SSL issuance silently
- **Missing `traefik.docker.network`** — container has router/service labels but no network pointer → Traefik can't route
- **Multiple services without explicit `service` linkage** — `Router X cannot be linked automatically with multiple Services`

## Diagnostic: Verifying a Container Is Actually Listening on Its Exposed Port

Port mapping in `docker ps` only means Docker published the port to the host. The **application inside** may still bind to `127.0.0.1` only, making it unreachable from Traefik (which connects via the Docker bridge `172.x.x.x`).

**Check from the host:**
```bash
# See what Docker mapped externally
docker port <container-name>
```

**Check from inside the container** (works even without `ss`/`netstat`):
```bash
# Verify the process is listening on the claimed port in hex
docker exec <container> sh -c "cat /proc/net/tcp | grep -i $(printf '%04X' <port>)"
# No output = the application is NOT listening on 0.0.0.0:port (likely loopback-only)
```

**Also check with /proc/*/fd:**
```bash
docker exec <container> sh -c "ls -la /proc/*/fd 2>/dev/null | grep -E 'socket:|\.:' | head -20"
# Shows open socket descriptors (rough proxy for listening sockets)
```

If the port is unclaimed but the app should be running, check its own config for `bind: loopback` or `host: 127.0.0.1`.

## Diagnostic: DNS Subdomain Validation

Before declaring a Traefik route broken, confirm the subdomain actually resolves. If DNS is missing, Let's Encrypt will fail with `NXDOMAIN` (visible in Traefik logs) and the route will never serve HTTPS.

```bash
for sub in design hub paperclip openclaw camofox; do
  echo -n "$sub.somosflux.com.br: "
  curl -sI --connect-timeout 3 "https://$sub.somosflux.com.br" 2>&1 | head -1 || echo "FAIL/DNS"
done
```

**If `dig` is unavailable inside the container**, `curl --connect-timeout` is a universal fallback that tests both DNS resolution + HTTPS reachability. A "connection timeout" or "Could not resolve host" from curl confirms NXDOMAIN.

## Diagnostic: Checking for Process Zombies (Memory Leak Indicator)

When a container accumulates `<defunct>` processes, it has a child-reaping problem. This is common with Chromium/Chrome headless in Docker. The parent process (Node.js, Python, etc.) is not calling `waitpid()` on SIGCHLD, leaving zombie PIDs in the process table. These consume negligible memory individually but can exhaust PID limits and indicate deeper stability issues.

```bash
# Count zombies per container
docker exec <container> ps aux 2>/dev/null | grep defunct | wc -l

# Quick check across all running containers
for c in $(docker ps -q); do
  count=$(docker exec "$c" ps aux 2>/dev/null | grep -c defunct || echo 0)
  [ "$count" -gt 0 ] && echo "$(docker inspect --format '{{.Name}}' $c): $count zombies"
done
```

**Action threshold:** If a non-browser container (e.g., Node.js app server, Python backend) has >5 zombies, investigate. If a browser-automation container (Puppeteer, Camofox, Playwright) has >20 zombies, restart is usually the fastest fix — the zumbis will not be reaped without code changes.

## Verification

After creating routes, test from outside:
```bash
curl -sk -o /dev/null -w "%{http_code}" https://domain.com/
```

Check Traefik logs for certificate issuance and routing decisions:
```bash
docker logs <traefik> --tail 30
```

## End-to-End Workflow

When a user reports a Gateway Timeout on a custom domain, follow this sequence:

### Step 1: Diagnose the network split
```bash
# Check if target and Traefik share a network
docker inspect <target> --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}\n{{end}}'
docker inspect <traefik> --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}\n{{end}}'
```
If the networks differ, the root cause is confirmed.

### Step 2: Hot-plug the missing network
```bash
docker network connect <shared-network> <target-container>
```
No restart needed. Verify immediately:
```bash
docker exec <traefik> wget -qO- --timeout=5 http://<target>:<port>/
```

### Step 3: Preserve existing access
Before adding new domains, confirm the user wants to **keep** existing panel links and port mappings. The router container approach (below) is additive only.

### Step 4: Create router container for new domains
```bash
docker run -d --name <router> --network <traefik-network> \
  --restart unless-stopped \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=<traefik-network>" \
  -l "traefik.http.routers.<r1>.entrypoints=websecure" \
  -l "traefik.http.routers.<r1>.rule=Host(\`a.domain.com\`)" \
  -l "traefik.http.routers.<r1>.tls.certresolver=letsencrypt" \
  -l "traefik.http.routers.<r1>.service=<svc1>" \
  -l "traefik.http.services.<svc1>.loadbalancer.server.url=http://<target1>:<port1>" \
  ...repeat for each service... \
  busybox sleep infinity
```

### Step 5: Verify external access
```bash
curl -sk -o /dev/null -w "%{http_code}" https://a.domain.com/
curl -sk -o /dev/null -w "%{http_code}" https://b.domain.com/
```

## Related: Paperclip Auth & Origin Issues

When Paperclip returns "Invalid origin" or login fails with 403/401 on a custom domain, the root cause is almost always env var precedence — `PAPERCLIP_PUBLIC_URL` and `PAPERCLIP_ALLOWED_HOSTNAMES` env vars override the config.json values. See the `paperclip-admin` skill for full diagnosis and password reset workflow.

## Technique: Basic Authentication via Container Labels

When a service needs password protection but the File Provider auth directory is read-only (e.g., Hostinger panel mounts `/auth` as `ro`), embed the `htpasswd` hash directly in the container's Traefik labels.

### 1. Generate the hash
```bash
docker run --rm httpd:alpine htpasswd -nb <user> <password>
# Example output: flux:$apr1$H4cWVQT5$HFC1L/UCFvt5xCLy6Gbb/.
```

### 2. Escape `$` characters for Docker labels
Docker labels interpret `$` as variable substitution. Escape each `$` as `\$`:
- Raw: `flux:$apr1$H4cWVQT5$HFC1L/UCFvt5xCLy6Gbb/.`
- Escaped: `flux:\$apr1\$H4cWVQT5\$HFC1L/UCFvt5xCLy6Gbb/.`

### 3. Add labels to the service container
```bash
docker run -d \
  --name myservice \
  --network proxy \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.myservice.rule=Host(\`app.example.com\`)" \
  -l "traefik.http.routers.myservice.entrypoints=websecure" \
  -l "traefik.http.routers.myservice.tls.certresolver=letsencrypt" \
  -l "traefik.http.routers.myservice.service=myservice" \
  -l "traefik.http.services.myservice.loadbalancer.server.port=8080" \
  -l "traefik.http.routers.myservice.middlewares=myservice-auth" \
  -l "traefik.http.middlewares.myservice-auth.basicauth.users=flux:\$apr1\$H4cWVQT5\$HFC1L/UCFvt5xCLy6Gbb/." \
  myimage:tag
```

**Critical:** The `\$` escaping is required. If you pass the label via a shell command, each `$` in the hash MUST be prefixed with `\`. Otherwise the shell/Docker swallows the `$...` as an empty variable and auth fails silently (no prompt, or 401 with wrong password).

**Pitfall:** When the container is already running, you cannot add labels. You must **stop, remove, and recreate** the container with the full label set. Docker labels are immutable after creation.

---

## Technique: Full Redeploy with Labels + Middlewares

When a service was originally started without Traefik labels (e.g., AionUI started with only `-p 127.0.0.1:25808:25808`), upgrading it to full HTTPS + auth requires a complete redeploy:

```bash
# 1. Stop and remove the old container (data is safe in volumes)
docker stop aionui
docker rm aionui

# 2. Recreate with full Traefik label set
docker run -d \
  --name aionui \
  --network proxy \
  --restart unless-stopped \
  -p 127.0.0.1:25808:25808 \
  -e AIONUI_ALLOW_REMOTE=true \
  -e AIONUI_HOST=0.0.0.0 \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.aionui.rule=Host(\`hub.somosflux.com.br\`)" \
  -l "traefik.http.routers.aionui.entrypoints=websecure" \
  -l "traefik.http.routers.aionui.tls.certresolver=letsencrypt" \
  -l "traefik.http.services.aionui.loadbalancer.server.port=25808" \
  -l "traefik.http.routers.aionui.middlewares=aionui-auth" \
  -l "traefik.http.middlewares.aionui-auth.basicauth.users=flux:\$apr1\$..." \
  aionui:v1.9.25
```

**Verification after redeploy:**
```bash
curl -sIk -u flux:password https://hub.somosflux.com.br | head -5
# Expect: HTTP/2 200
```

## Related: Adding New Services to an Existing VPS

When the user already has Traefik + Hermes + other services running and wants to add a new service (e.g., AionUI, Open WebUI, a custom app), follow the workflow in `references/installing-new-services-on-vps.md`. Key points:

1. **Check DNS exists BEFORE creating the Traefik route** — Traefik/Let's Encrypt will fail validation if the subdomain doesn't resolve. Ask the user to add the A record in their DNS panel first.
2. **Extract .deb packages with `dpkg -x`** instead of installing directly — more reliable inside Docker containers than `dpkg -i`.
3. **Electron apps need Xvfb** — any desktop app running headless requires a virtual display.
4. **Always attach to `--network proxy`** — otherwise Traefik can't reach the new container.
5. **Use the File Provider** to add routes without touching the original docker-compose.
6. **For auth, prefer label-based basic auth** (see "Basic Authentication via Container Labels" above) when the File Provider auth directory is read-only.

## Diagnosing Infrastructure-Wide Instability (OOM, Memory Pressure, Swap)

When the user reports **intermittent loss of access to all services** (not just one), the root cause is typically resource exhaustion — RAM saturation triggering the Linux OOM Killer. This is especially common on Hostinger VPS deployments because they ship with **zero swap space**.

### Key symptoms
- Multiple services go down simultaneously and come back on their own
- Gateway logs show: `Exiting with code 1 (signal-initiated shutdown without restart request)`
- Occurs more frequently under heavy AI workloads (large context windows, concurrent sessions)
- Docker socket may or may not be available in the Hermes container

### Diagnostic steps when Docker IS available
```bash
# Check host memory
free -h
# Check container restart counts (high counts = frequent OOM kills)
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E "Restarting|[0-9]+ (seconds|minutes|hours) ago"
docker inspect $(docker ps -q) --format '{{.Name}} {{.RestartCount}}' | sort -t' ' -k2 -rn
# Check for OOM events in kernel log
dmesg | grep -i "out of memory\|oom"
```

### Diagnostic steps when Docker is NOT available
See `references/hostinger-resource-constraints.md` for the full methodology, including:
- Reading `/proc/meminfo` for RAM and swap status
- HTTP health checks to public endpoints to verify which services are up
- Gateway/error log analysis for crash signatures
- Session history search to avoid re-diagnosing known issues

### Host access from inside the Hermes container

When running diagnostics or fixes that require host-level access (creating swap, editing `/etc/fstab`, checking `dmesg` for OOM), you're inside the Hermes container which does NOT have host namespace access. Two approaches:

1. **`nsenter`** — often fails with `Operation not permitted` inside Docker:
   ```bash
   nsenter -t 1 -m -u -i -n -- sh -c 'free -h'
   # → nsenter: reassociate to namespaces failed: Operation not permitted
   ```

2. **`docker run --privileged`** — works reliably when Docker socket is mounted:
   ```bash
   docker run --rm --privileged --pid=host -v /:/host alpine sh -c '
     free -h | head -3
     swapon --show
     cat /host/etc/fstab
   '
   ```
   This launches a temporary Alpine container with full host access. The `-v /:/host` mount lets you read/write host files via `/host/` prefix. **Always pull Alpine first** — it won't exist locally on first use.

   **Key commands for host-level fixes:**
   ```bash
   # Create 4GB swap (persists across reboots)
   docker run --rm --privileged --pid=host -v /:/host alpine sh -c '
     fallocate -l 4G /host/swapfile
     chmod 600 /host/swapfile
     mkswap /host/swapfile
     swapon /host/swapfile
     grep -q swapfile /host/etc/fstab || echo "/swapfile none swap sw 0 0" >> /host/etc/fstab
   '

   # Set container memory limits (no restart needed)
   docker update --memory=3072m --memory-swap=-1 hermes-flux
   docker update --memory=2048m --memory-swap=-1 openclaw-xxx
   docker update --memory=1024m --memory-swap=-1 paperclip-xxx
   ```

### The fix
1. **Create swap** on the host (4GB minimum) — this alone prevents ~90% of OOM outages
2. **Set container memory limits** to prevent any single service from consuming all RAM
3. **Verify restart policies** (`restart: unless-stopped`) on all containers
4. **Mount Docker socket** in Hermes container so it can self-monitor and auto-heal

### Quick all-services health check (no Docker needed)
```bash
for svc in "openclaw.somosflux.com.br" "paperclip.somosflux.com.br" "hub.somosflux.com.br" "hermes.somosflux.com.br"; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://$svc/")
  echo "$svc → HTTP $code"
done
```

## VPS Gap Analysis (Full Infrastructure Audit)

When the user asks to "analyze the entire VPS structure", "find gaps", "audit infrastructure", or similar system-wide health checks, this is a 7-area systematic scan — not just Docker cleanup. Run the dedicated script for a structured report:

```bash
bash /opt/data/skills/devops/docker-traefik-routing/scripts/vps-gap-analysis.sh
```

### The 7 areas (scan all, report all)
1. **System resources** — CPU, RAM, swap, disk, load average
2. **Docker** — containers, status, memory/CPU per container, restart policies & limits, restart counts
3. **Network** — listening ports, DNS config, Docker networks, exposed interfaces
4. **Security** — firewall, 0.0.0.0 bindings, hardcoded secrets in compose files
5. **Service health** — OpenClaw version/plugin/DNS errors, Hermes vision/gateway errors, Paperclip restarts
6. **Backups & resilience** — crontabs, timers, volume inventory (which have no backup?), restart policies
7. **Disk & cleanup** — images (dangling, unused), reclaimable space, stopped containers

### Fixes applied (2026-05-09 session)
- ✅ **4GB swap** created at `/swapfile`, persisted in `/etc/fstab`
- ✅ **Container memory limits** set: Hermes 3GB, OpenClaw 2GB, Paperclip 1GB, WebUI 512MB, Traefik 256MB
- ✅ **OpenClaw DNS fixed**: `ollama` provider `baseUrl` changed from `api.nousresearch.com` (dead) to `opencode.ai/zen/go/v1`
- ✅ **OpenClaw plugins cleaned**: 5 failing plugins disabled (acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft)
- ✅ **Disk cleaned**: dangling image (8.91GB) + aionui:v1.9.25 (1.94GB) removed → ~2.3GB recovered
- ✅ **Hermes vision provider**: set to `opencode-go/glm-5.1` (supports text+image input)

### Key pitfalls discovered (2026-05-09)
- **OpenClaw DNS failures**: `api.nousresearch.com` unresolvable → failover adds 26s latency. Fix: add public DNS (8.8.8.8) to container config.
- **Vision provider misconfigured**: DeepSeek doesn't support `image_url` → BadRequest on every vision call. Fix: configure a vision-capable model explicitly.
- **OpenClaw plugins failing silently**: `acpx, amazon-bedrock, amazon-bedrock-mantle, browser, microsoft` all fail validation on startup. Fix: remove unused plugins.
- **Hardcoded passwords in compose**: `HERMES_WEBUI_PASSWORD` in plaintext. Fix: use `.env` or Docker secrets.
- **Zero backups**: no crontabs, no timers, critical volumes unprotected. Fix: schedule daily volume + config backup.
- **aionui:v1.9.25 image (1.94GB)** orphaned with no running container.

### Gap severity classification
| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Service can fail now | Fix immediately |
| 🟡 High | Functionality impaired | Fix within 24h |
| 🟠 Medium | Data/security risk | Fix within 1 week |
| 🟢 Low | Monitor | Address when convenient |

### Reporting format
Present findings grouped by severity with:
- Gap title + one-line explanation
- Current state (with evidence)
- Recommended fix
- Number the gaps for reference (user says "fix gap 3")

See `references/session-2026-05-09-vps-gap-analysis.md` for the full findings from the first gap analysis session.

## Related: Docker Audit & Cleanup

When the user asks to "analyze for duplicates and unused resources", run this audit before any removal:

```bash
# Full inventory
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'
docker volume ls
docker network ls

# Check which images are actually in use
docker ps -a --format '{{.Image}}' | sort -u

# Check orphaned volumes
docker volume ls -q | while read v; do
  used_by=$(docker ps -a --filter volume=$v --format '{{.Names}}')
  echo "$v | Used by: ${used_by:-NONE}"
done

# Check networks with no containers
docker network ls --format '{{.Name}}' | while read n; do
  count=$(docker network inspect $n --format '{{len .Containers}}')
  [ "$count" = "0" ] && echo "$n: EMPTY"
done
```

Remove with caution, confirming each item:
- **Stopped containers** — only if they conflict with active ones (same bind mount)
- **Unused images** — verify not referenced by any container first
- **Dangling images** — safe to prune with `docker image prune -f`
- **Orphaned volumes** — only if `Used by: NONE`
- **Empty networks** — safe to remove unless they are default Docker networks

## References

- `references/hostinger-vps-notes.md` — Environment specifics for Hostinger Docker Compose Catalog setups
- `references/hostinger-resource-constraints.md` — OOM, swap, memory pressure diagnosis; diagnostic methodology when Docker socket is unavailable
- `references/hostinger-vps-gap-analysis-checklist.md` — Systematic VPS diagnostic checklist: resources, Docker, network/DNS, security, service configs, backups
- `references/session-2026-05-08-error-transcript.md` — Real error logs and fix confirmation from a live session
- `references/session-2026-05-08-network-reconnect-fix.md` — Case study: container recreation by managed panel erasing runtime network attachments, and the auto-healing monitor solution
- `references/session-2026-05-08-evening-recurrence.md` — Recurrence validation ~5 hours later; proves panel recreation is repeated, not one-time; pre-diagnosis workflow lesson
- `references/session-2026-05-09-vps-gap-analysis.md` — Full 13-gap analysis from first infrastructure audit: findings, commands, severity classifications, fix priority order
- `references/session-2026-05-09-vps-gap-analysis-applied.md` — All fixes applied (swap, memory limits, OpenClaw DNS/plugins, vision provider, disk cleanup) with exact commands and pitfalls
- `references/headless-electron-docker.md` — Running Electron/desktop apps in Docker with Xvfb (e.g., AionUI on a headless VPS)
- `references/aionui-deployment-pitfalls.md` — AionUI-specific discoveries: no Portuguese locale, no Hermes Agent support, dual auth layers, OpenClaw gateway bind, DNS ordering, label immutability
- `references/open-design-deployment.md` — Open Design (nexu-io/open-design) Docker deployment on VPS: container setup, health check, port exposure, network connectivity, Traefik labels
- `templates/traefik-router-container.sh` — Quick router container label template
- `scripts/docker-audit.sh` — Runnable audit script to identify duplicates, orphans, and empty Docker resources before cleanup
- `scripts/vps-gap-analysis.sh` — Full 7-area infrastructure gap analysis (resources, Docker, network, security, services, backups, disk) with color-coded severity output
- `scripts/network-monitor.sh` — Generic self-healing monitor that auto-reconnects containers to the Traefik network if detached
