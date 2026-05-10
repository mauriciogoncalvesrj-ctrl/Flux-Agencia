# Hostinger VPS — Docker Compose Catalog Notes

## Environment Characteristics
- VPS comes with Hostinger's Docker Compose Catalog (managed panel)
- Docker compose files are NOT directly editable on disk (managed by Hostinger)
- Services get auto-generated Traefik labels pointing to `srvXXXX.hstgr.cloud` subdomains
- Each service exposes a random high port on the host (e.g., 57186, 64551)
- The panel provides "Abrir" links that open these ports directly
- User frequently clicks the panel **"Atualizar"** button, which recreates containers

## User Preference
- **Preserve** the Hostinger panel "Abrir" links and existing port access
- **Add** custom domains (e.g., `*.somosflux.com.br`) alongside existing routes
- Do NOT remove or replace the `srvXXXX.hstgr.cloud` labels
- Explanations should be simple — user self-describes as having limited knowledge

## Known Services in This Environment
| Service | Container Name | Internal Port | External Port | Image |
|---|---|---|---|---|
| Hermes Agent | `hermes-flux` | 9119 | 8642 | `nousresearch/hermes-agent:latest` |
| OpenClaw | `openclaw-4vbk-openclaw-1` | 64551 | 64551 | `ghcr.io/hostinger/hvps-openclaw:latest` |
| Paperclip | `paperclip-tjjz-paperclip-1` | 3100 | 57186 | `ghcr.io/hostinger/hvps-paperclip:latest` |
| Traefik | `flux-traefik` | 80/443 | 80/443 | `traefik:v3.6` |

## Traefik Configuration
- Uses CLI flags (no config file)
- Let's Encrypt with HTTP challenge
- Network: `proxy`
- Cert email: `mauriciogoncalvesrj@gmail.com`
- **File Provider enabled** for persistent custom routes — reads `/letsencrypt/*.yaml`

## Adding Custom Domains (Definitive Method)
Instead of router containers, create a YAML file in `/letsencrypt/` (persisted host volume):
```yaml
http:
  routers:
    myapp:
      rule: 'Host(`app.somosflux.com.br`)'
      entryPoints: [websecure]
      service: myapp
      tls: { certResolver: letsencrypt }
  services:
    myapp:
      loadBalancer:
        servers:
          - url: 'http://target-container:port'
```
Traefik must be started with `--providers.file.directory=/letsencrypt/ --providers.file.watch=true`.

## DNS
- `somosflux.com.br` → VPS IP
- Subdomains: `hermes`, `openclaw`, `paperclip`, `traefik`

## Network Map (final state)
| Container | Networks | IP on proxy |
|---|---|---|
| hermes-flux | hermes-agent-84im_default, proxy | 172.18.0.3 |
| openclaw-4vbk-openclaw-1 | hermes-net, proxy | 172.18.0.5 |
| paperclip-tjjz-paperclip-1 | hermes-net, proxy | 172.18.0.7 |
| flux-traefik | proxy | 172.18.0.2 |
