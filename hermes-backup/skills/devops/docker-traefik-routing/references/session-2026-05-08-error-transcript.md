# Session Error Transcript — 2026-05-08

## Scenario
User trying to access Hermes Agent dashboard at `hermes-agent-84im.srv1651876.hstgr.cloud` got **Gateway Timeout**.

## Diagnosis Steps

### 1. Check if backend responds locally
```bash
curl -sk -o /dev/null -w "%{http_code}" http://localhost:9119/
# => 200 (backend is healthy)
```

### 2. Check container networks
```bash
docker inspect hermes-flux --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} | {{$v.IPAddress}}\n{{end}}'
# => hermes-agent-84im_default | 172.16.1.2
#    (NO proxy network!)

docker inspect flux-traefik --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} | {{$v.IPAddress}}\n{{end}}'
# => proxy | 172.18.0.2
```

### 3. Test from Traefik
```bash
docker exec flux-traefik wget -qO- --timeout=5 http://hermes-flux:9119/
# => wget: bad address 'hermes-flux:9119'
```

**Root cause:** Containers on different networks. Traefik cannot resolve container name.

## Fix 1: Hot-plug network connection
```bash
docker network connect proxy hermes-flux
```
Verify:
```bash
docker exec flux-traefik wget -qO- --timeout=5 http://hermes-flux:9119/
# => <!doctype html>... (success)
```

## Fix 2: Router container for new domains
User wanted custom domains (`*.somosflux.com.br`) alongside existing Hostinger panel links.
Created router container with multiple routes.

### First attempt FAILED
```bash
docker run -d --name somosflux-router --network proxy ...
  -l "traefik.http.services.hermes-somosflux.loadbalancer.server.url=http://hermes-flux:9119"
  -l "traefik.http.services.openclaw-somosflux.loadbalancer.server.url=http://openclaw-4vbk-openclaw-1:64551"
  -l "traefik.http.services.paperclip-somosflux.loadbalancer.server.url=http://paperclip-tjjz-paperclip-1:3100"
```

**Error in Traefik logs:**
```
ERR Router openclaw-somosflux cannot be linked automatically with multiple Services: ["hermes-somosflux" "openclaw-somosflux" "paperclip-somosflux"]
```

### Second attempt SUCCEEDED
Added explicit `.service` linkage on each router:
```
traefik.http.routers.hermes-somosflux.service=hermes-somosflux
traefik.http.routers.openclaw-somosflux.service=openclaw-somosflux
traefik.http.routers.paperclip-somosflux.service=paperclip-somosflux
```

Verify:
```bash
curl -sk -o /dev/null -w "%{http_code}" https://hermes.somosflux.com.br/
# => 200
curl -sk -o /dev/null -w "%{http_code}" https://openclaw.somosflux.com.br/
# => 200
curl -sk -o /dev/null -w "%{http_code}" https://paperclip.somosflux.com.br/
# => 200
```

## Key Lessons
1. Always verify containers share the same Traefik network
2. When multiple services exist on one container, ALWAYS add explicit `traefik.http.routers.<name>.service=<svc-name>`
3. Router container with `loadbalancer.server.url` preserves original labels — no docker-compose edits needed
