# Headless Electron Apps in Docker (VPS Pattern)

> Technique: Run desktop/Electron applications on a headless VPS by providing a virtual display (Xvfb) inside a custom Docker container.
> Example: AionUI v1.9.25 (Electron-based multi-agent UI) installed on a Hostinger VPS.
> Date: 2026-05-08

---

## Problem

You want to run a desktop application (built with Electron, Qt, GTK, etc.) on a VPS that has no physical display. The app crashes with errors like:
- `Error: Cannot open display`
- `The futex facility returned an unexpected error code`
- `GPU process isn't usable`

## Solution: Xvfb + No-Sandbox

Create a Docker image that:
1. Installs Xvfb (X virtual framebuffer)
2. Installs the app's dependencies
3. Starts Xvfb before the app
4. Runs the app with `--no-sandbox` (Electron-specific)

---

## Step-by-Step: AionUI Example

### 1. Download the .deb package

```bash
cd /tmp
wget https://github.com/iOfficeAI/AionUi/releases/download/v1.9.25/AionUi-1.9.25-linux-amd64.deb
```

### 2. Create Dockerfile

```dockerfile
FROM debian:bookworm-slim

# Install Xvfb + Electron dependencies
RUN apt-get update && apt-get install -y \
    xvfb libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 \
    xdg-utils libatspi2.0-0 libuuid1 libsecret-1-0 \
    libgbm1 libxcb-dri3-0 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Extract .deb (don't install — avoids systemd hooks)
COPY AionUi-1.9.25-linux-amd64.deb /tmp/
RUN dpkg -x /tmp/AionUi-1.9.25-linux-amd64.deb /opt/aionui \
    && rm /tmp/AionUi-1.9.25-linux-amd64.deb

# Expose webui port
EXPOSE 25808

# Entrypoint: start Xvfb, then app
COPY start.sh /start.sh
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]
```

### 3. Create start.sh

```bash
#!/bin/bash
# Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1280x720x24 &
sleep 2

# Start AionUI with webui + no-sandbox
exec /opt/aionui/usr/bin/aionui \
  --webui --remote --no-sandbox \
  "$@"
```

### 4. Build and run

```bash
# Build
cd /tmp/aionui-install
docker build -t aionui:v1.9.25 .

# Run (attach to Traefik network)
docker run -d --name aionui \
  --network proxy \
  -p 25808:25808 \
  -v /opt/data/aionui-data:/data \
  -e ALLOW_REMOTE=true \
  aionui:v1.9.25
```

### 5. Add Traefik route (File Provider)

```yaml
# In /letsencrypt/somosflux.yml (or Traefik-mounted volume)
http:
  routers:
    aion-somosflux:
      rule: 'Host(`aion.somosflux.com.br`)'
      entryPoints: [websecure]
      service: aion-somosflux
      tls:
        certResolver: letsencrypt

  services:
    aion-somosflux:
      loadBalancer:
        servers:
          - url: 'http://aionui:25808'
```

---

## Key Pitfalls

1. **Use `dpkg -x`, not `dpkg -i`** inside Docker
   - `dpkg -i` tries to run postinst scripts that may call systemd
   - `dpkg -x` just extracts files to a directory

2. **Electron needs `--no-sandbox`** in Docker
   - Without it: `GPU process isn't usable`
   - Add to entrypoint script or wrapper

3. **Xvfb needs the `screen` argument**
   - `Xvfb :99` alone may fail
   - Use: `Xvfb :99 -screen 0 1280x720x24 &`

4. **Export DISPLAY before starting the app**
   - `export DISPLAY=:99` must happen in the same shell/process tree

5. **Some apps need additional libs**
   - If the app still fails, check `ldd /path/to/binary` for missing libraries
   - Common missing ones: `libgbm1`, `libxshmfence1`, `libatspi2.0-0`

---

## Generic Template

Replace `APP_NAME`, `APP_PORT`, `APP_BINARY`:

```dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y \
    xvfb libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 \
    xdg-utils libatspi2.0-0 libuuid1 libsecret-1-0 \
    libgbm1 libxcb-dri3-0 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*
COPY your-app.deb /tmp/
RUN dpkg -x /tmp/your-app.deb /opt/app && rm /tmp/your-app.deb
EXPOSE APP_PORT
COPY start.sh /start.sh
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]
```

```bash
#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1280x720x24 &
sleep 2
exec /opt/app/usr/bin/YOUR_BINARY --no-sandbox "$@"
```

---

## Verification

```bash
# Check Xvfb is running
docker exec aionui pgrep -a Xvfb

# Check app is listening
docker exec aionui netstat -tlnp | grep 25808

# Test from Traefik network
docker run --rm --network proxy busybox \
  wget -qO- --timeout=5 http://aionui:25808
```
