# Installing New Services on a Hostinger VPS and Exposing via Traefik

When the user wants to add a new service to their existing VPS (already running Hermes, OpenClaw, Paperclip, Traefik), follow this workflow.

## Pre-Flight Checklist

1. **Check available resources** — RAM, disk, CPU:
   ```bash
   free -h && df -h / && nproc
   ```

2. **Verify Traefik File Provider is active**:
   ```bash
   docker inspect flux-traefik --format='{{json .Config.Cmd}}' | grep 'providers.file'
   ```
   If missing, the Traefik container was recreated by the panel and lost the flag. Must recreate Traefik with `--providers.file.directory=/letsencrypt/ --providers.file.watch=true`.

3. **Check DNS** — BEFORE creating Traefik routes, verify the subdomain exists:
   ```bash
   host newdomain.somosflux.com.br || nslookup newdomain.somosflux.com.br
   curl -sI https://newdomain.somosflux.com.br 2>&1 | head -5
   ```
   If DNS returns nothing or NXDOMAIN, tell the user to create an **A record** in the Hostinger panel pointing to the server IP (`2.24.85.2` in this environment).

## Installation Pattern

### Step 1: Download and inspect the package

Most services distribute as `.deb`, `.tar.gz`, or Docker images.

```bash
# Create temp workspace
mkdir -p /tmp/service-install && cd /tmp/service-install

# Download (use curl -L to follow redirects)
curl -L -o package.deb "https://github.com/OWNER/REPO/releases/download/vX.Y.Z/package.deb"
ls -lh package.deb
```

**Pitfall:** GitHub `latest/download` URLs redirect to versioned URLs. Use `curl -L` (follow redirects) or query the API first to get the exact asset URL.

### Step 2: Extract if not installable directly

If `dpkg -i` fails due to missing dependencies or permission issues inside a container, extract the `.deb` manually:

```bash
# Extract .deb contents
dpkg -x package.deb /tmp/service-extract

# Inspect structure
find /tmp/service-extract -maxdepth 3 -type d
```

This yields the files as they would be installed on a normal system (typically under `/opt/SERVICE/` and `/usr/share/`).

### Step 3: Build a Docker image

Create a minimal Dockerfile that copies the extracted binaries and installs runtime dependencies:

```dockerfile
FROM debian:bookworm-slim

# Install runtime dependencies (adjust per service)
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb libgtk-3-0 libnss3 libasound2 libgbm1 libxshmfence1 \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Copy extracted service
COPY opt/ServiceName /opt/ServiceName

# Create data/workspace dirs
RUN mkdir -p /data /workspace

# Environment
ENV DATA_DIR=/data
ENV ALLOW_REMOTE=true

# Expose service port
EXPOSE 25808

# Startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh /opt/ServiceName/ServiceName

WORKDIR /workspace
CMD ["/start.sh"]
```

**For Electron apps** (like AionUI), add `xvfb` and a virtual display startup in `start.sh`:
```bash
#!/bin/bash
Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
sleep 2
/opt/ServiceName/ServiceName --webui --remote --no-sandbox --disable-gpu
```

### Step 4: Build and run

```bash
cd /tmp/service-install
docker build -t servicename:vX.Y.Z .

docker run -d --name servicename \
  --network proxy \
  -p 25808:25808 \
  -v /opt/data/service-data:/data \
  -e ALLOW_REMOTE=true \
  servicename:vX.Y.Z
```

**Always use `--network proxy`** so Traefik can reach the container by name.

### Step 5: Add Traefik route via File Provider

Edit `/letsencrypt/somosflux.yml` inside the Traefik container:

```yaml
http:
  routers:
    service-somosflux:
      rule: 'Host(`service.somosflux.com.br`)'
      entryPoints:
        - websecure
      service: service-somosflux
      tls:
        certResolver: letsencrypt

  services:
    service-somosflux:
      loadBalancer:
        servers:
          - url: 'http://servicename:25808'
```

**Pitfall — YAML escaping with backticks:**
When writing via `docker exec`, single-quote the YAML rule and escape backticks:
```bash
docker exec -i flux-traefik sh -c "cat >> /letsencrypt/somosflux.yml << 'EOF'
    service-somosflux:
      rule: 'Host(\`service.somosflux.com.br\`)'
EOF"
```

### Step 6: Verify

1. Container health (internal):
   ```bash
   docker run --rm --network proxy busybox wget -qO- --timeout=5 http://servicename:25808
   ```

2. DNS propagation:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" --max-time 15 https://service.somosflux.com.br/
   ```

3. If DNS fails (HTTP 000), the A record doesn't exist yet. Tell the user to create it in the Hostinger panel.

## Case Study: AionUI

**Service:** AionUI v1.9.25 (Electron app, 239MB .deb)
**Challenge:** Electron needs a display server; VPS is headless
**Solution:** Xvfb virtual display inside Docker container
**Network:** `--network proxy` for Traefik connectivity
**Port:** 25808 (AionUI Linux .deb default)
**DNS:** `aion.somosflux.com.br` → A → 2.24.85.2
**Result:** WebUI accessible via HTTPS through Traefik

## Common Pitfalls

1. **DNS not created before Traefik route** — Traefik will attempt Let's Encrypt validation and fail if the domain doesn't resolve. Always create DNS first.

2. **Port binding conflicts** — Check `docker ps` to ensure the host port isn't already in use.

3. **Missing `--network proxy`** — If the container isn't on the proxy network, Traefik returns 502.

4. **Electron apps need Xvfb** — Any Electron-based service (AionUI, Discord bots, etc.) requires a virtual display on headless servers.

5. **.deb extraction vs installation** — Inside Docker containers, `dpkg -i` often fails due to missing systemd or permission issues. Extracting with `dpkg -x` and building a custom image is more reliable.

6. **Hostinger panel recreates containers** — Any manual `docker run` for the new service is safe, but if the panel has a "catalog" entry for it, a panel update may conflict. Prefer Docker Compose or standalone `docker run` outside the panel's management.
