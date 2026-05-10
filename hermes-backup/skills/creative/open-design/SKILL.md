---
name: open-design
description: "Deploy, configure, and use Open Design (nexu-io/open-design) — the open-source alternative to Claude Design. 111 skills, 72 design systems, local-first, BYOK. Generates web prototypes, carousels, landing pages, presentations, emails, videos, and more via coding-agent CLIs or API proxy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [open-design, design, prototype, carousel, landing-page, presentation, creative, docker]
    homepage: https://github.com/nexu-io/open-design
    related_skills: [claude-design, social-media-carousels, sketch, popular-web-designs]
---

# Open Design

Open Design (OD) is the open-source alternative to Anthropic's Claude Design. It runs a local daemon + Next.js web app that delegates design generation to coding-agent CLIs (Hermes, Claude Code, Codex, etc.) or a BYOK API proxy. It ships with **111 skills** and **72 brand-grade design systems**.

**This skill covers deployment on Docker, configuration, and integration with the Flux agency pipeline.**

---

## Quick Facts

- **Docker image:** `docker.io/vanjayak/open-design:latest`
- **Container name:** `open-design`
- **Port:** 7456 (configurable via `OD_PORT`)
- **Network:** Must be on the same Docker network as Traefik (e.g., `proxy`)
- **RAM:** 384MB minimum, 512MB recommended
- **Health endpoint:** `GET /api/health` → `{"ok":true,"version":"0.5.0"}`
- **Skills endpoint:** `GET /api/skills` → JSON with `skills` array
- **Design systems endpoint:** `GET /api/design-systems`
- **Config/data:** Volume `open_design_data` at `/app/.od`
- **Node.js:** Requires Node ~24 (image bundles it; local dev needs nvm)
- **GitHub:** https://github.com/nexu-io/open-design (35K+ stars)
- **Docs:** https://docs.openclaw.ai (note: OpenClaw docs, not OD-specific)

---

## Docker Deployment

### Minimal Container

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
  docker.io/vanjayak/open-design:latest
```

### With Traefik HTTPS + Custom Domain

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
  -e "OD_ALLOWED_ORIGINS=https://design.example.com" \
  --memory=512m \
  --pids-limit=256 \
  -v open_design_data:/app/.od \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.open-design.rule=Host(\`design.example.com\`)" \
  -l "traefik.http.routers.open-design.entrypoints=websecure" \
  -l "traefik.http.routers.open-design.tls=true" \
  -l "traefik.http.routers.open-design.tls.certresolver=letsencrypt" \
  -l "traefik.http.services.open-design.loadbalancer.server.port=7456" \
  docker.io/vanjayak/open-design:latest
```

**DNS requirement:** Create an A record for `design.example.com` pointing to the server IP before starting.

### Health Check

```bash
# Inside container
docker exec open-design wget -qO- http://127.0.0.1:7456/api/health
# Expected: {"ok":true,"version":"0.5.0"}

# From another container on the same network
curl http://172.18.0.7:7456/api/health
```

### Port Exposure Note

When running inside a Docker container (e.g., Hermes Agent), `localhost:7456` may not reach the Open Design container because they're on different networks. Use the container's Docker network IP instead:

```bash
OD_IP=$(docker inspect open-design --format '{{range $k,$v := .NetworkSettings.Networks}}{{$v.IPAddress}}{{end}}')
curl "http://${OD_IP}:7456/api/health"
```

---

## Skills Relevant to Marketing Agencies

### High-Value Skills for Clinics/E-commerce

| Skill | Mode | What It Produces |
|-------|------|-----------------|
| `social-carousel` | prototype | 3-card 1080×1080 Instagram carousel |
| `email-marketing` | prototype | Brand product-launch HTML email |
| `saas-landing` | prototype | Landing page with hero, features, pricing, CTA |
| `magazine-poster` | prototype | Editorial-style poster |
| `video-shortform` | video | 3-10s clips for Reels/TikTok |
| `image-poster` | image | Poster, key art, editorial illustration |
| `audio-jingle` | audio | Jingles, beds, voiceover, sound effects |
| `mobile-app` | prototype | Mobile app screen in iPhone 15 Pro frame |
| `blog-post` | prototype | Long-form editorial article |
| `finance-report` | prototype | Quarterly financial report |
| `guizang-ppt` | deck | Magazine-style web PPT |
| `simple-deck` | deck | Minimal horizontal-swipe deck |
| `weekly-update` | deck | Team weekly cadence deck |
| `invoice` | prototype | Single-page invoice |
| `dashboard` | prototype | Admin/analytics dashboard |
| `motion-frames` | prototype | Motion-design hero with CSS animations |
| `tweaks` | prototype | Side panel of live parameterized controls |
| `critique` | prototype | 5-dimension design self-critique |

### Design Systems Available (72 built-in)

Stripe, Linear, Vercel, Airbnb, Tesla, Notion, Apple, Anthropic, Cursor, Supabase, Figma, Resend, Raycast, Lovable, Cohere, Mistral, ElevenLabs, X.AI, Spotify, Webflow, Sanity, PostHog, MongoDB, ClickHouse, and more.

---

## Configuration

### Agent Motor (Settings → Execution & model)

OD needs a "motor" — a coding agent or API — to generate artifacts. Options:

1. **BYOK API Proxy** (no CLI needed): In Settings, choose a provider (OpenAI, Anthropic, Azure, Google) and paste API key + model. The daemon normalizes requests.

2. **Hermes Agent CLI**: If `hermes` is on PATH, OD auto-detects it on startup and makes it available in the model picker.

3. **Claude Code, Codex, Gemini CLI, OpenCode, etc.**: Any supported CLI on PATH is auto-detected.

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OD_BIND_HOST` | Host to bind (use `0.0.0.0` for Docker) | `127.0.0.1` |
| `OD_PORT` | Daemon + web port | `7456` |
| `OD_WEB_PORT` | Web UI port override | Same as `OD_PORT` |
| `OD_ALLOWED_ORIGINS` | CORS origins (comma-separated) | `""` (none) |
| `NODE_OPTIONS` | Node.js flags (e.g., `--max-old-space-size=384`) | unset |
| `NODE_ENV` | Production mode | `development` |

---

## Local Development (Not Docker)

If you need to hack on OD itself or run it outside Docker:

```bash
# Requires Node 22+ and pnpm 10.33+
nvm install 22
nvm use 22
npm install -g pnpm@latest

git clone https://github.com/nexu-io/open-design.git
cd open-design
pnpm install

# Start daemon + web (no desktop)
OD_SKIP_DESKTOP=1 pnpm tools-dev start
```

**Pitfall:** The desktop (Electron) app will fail on headless servers. Use `OD_SKIP_DESKTOP=1` or the Docker image instead.

**Pitfall:** pnpm latest requires Node.js 22+. If you're on Node 20, install via nvm first:

```bash
export NVM_DIR="$HOME/.nvm"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source "$NVM_DIR/nvm.sh"
nvm install 22
nvm use 22
npm install -g pnpm@latest
```

---

## Integration with OpenClaw

OpenClaw can use Open Design's API as an MCP-like tool or the design output can be consumed directly. Potential integration patterns:

1. **OpenClaw Telegram bot** → receives design request → calls Open Design API (`POST /api/chat`) → returns artifact
2. **Hermes cron job** → triggers content generation pipeline → sends carousel brief to Open Design → saves output
3. **Manual**: User opens `https://design.example.com`, picks a skill and design system, types brief, gets artifact

---

## Troubleshooting

### Container exits immediately
- Check `OD_BIND_HOST=0.0.0.0` — default `127.0.0.1` won't work in Docker
- Check memory: `docker stats open-design` — if exceeding 512MB, increase `--memory`

### Can't reach from other containers
- Ensure both containers are on the same Docker network (`docker network connect proxy open-design`)
- Use the container IP, not `localhost`

### Desktop Electron fails on headless server
- Use `OD_SKIP_DESKTOP=1` or the Docker image (no desktop at all)
- The `pnpm tools-dev start` command tries to start desktop and fails — use Docker instead

### Skills not showing
- OD auto-detects skills from the `skills/` directory on startup
- Restart the container after changing skills

---

## References

- `references/open-design-skills-catalog.md` — Full list of 111 skills with descriptions, modes, and scenarios