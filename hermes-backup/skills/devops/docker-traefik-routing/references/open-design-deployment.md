# Open Design Deployment on VPS

## Overview
Open Design (nexu-io/open-design) is a design generation tool with 111 skills and 72 design systems. Deployed as a Docker container behind Traefik.

## Deployment Details (2026-05-09)

### Container Setup
```bash
docker run -d \
  --name open-design \
  --restart always \
  --network proxy \
  -p 7456:7456 \
  -e NODE_ENV=production \
  -e "NODE_OPTIONS=--max-old-space-size=384" \
  -e OD_BIND_HOST=0.0.0.0 \
  -e OD_PORT=7456 \
  -e OD_WEB_PORT=7456 \
  --memory=512m \
  --pids-limit=256 \
  -v open_design_data:/app/.od \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.open-design.rule=Host(\`design.somosflux.com.br\`)" \
  -l "traefik.http.routers.open-design.entrypoints=websecure" \
  -l "traefik.http.routers.open-design.tls=true" \
  -l "traefik.http.routers.open-design.tls.certresolver=letsencrypt" \
  -l "traefik.http.services.open-design.loadbalancer.server.port=7456" \
  docker.io/vanjayak/open-design:latest
```

### Key Pitfalls

1. **OD_BIND_HOST must be 0.0.0.0** — Default is 127.0.0.1 which makes the app unreachable from other containers.

2. **Container network isolation** — Must be on same Docker network as Traefik. Use `--network proxy` or `docker network connect proxy open-design`.

3. **localhost:7456 doesn't work from other containers** — Use container Docker network IP (172.18.0.x) or Traefik domain.

4. **DNS required for Traefik HTTPS** — Create A record before starting. Without DNS, Let's Encrypt fails.

5. **Health check** — `GET /api/health` returns `{"ok":true,"version":"0.5.0"}`.

6. **Desktop mode fails on headless servers** — Use `OD_SKIP_DESKTOP=1` or Docker image.

7. **Node.js version** — Local dev requires Node 22+. Node 20 causes ERR_UNKNOWN_BUILTIN_MODULE with pnpm.

8. **No docker compose inside Hermes container** — Use `docker run` directly.