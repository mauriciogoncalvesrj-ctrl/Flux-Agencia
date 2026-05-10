# OpenClaw Custom Providers & Traefik Domain Setup — Session 2026-05-09

## What this reference covers

- Adding **Ollama Cloud** and **Opencode Go** as custom providers via `models.providers`
- Configuring **custom domain access** (`https://openclaw.somosflux.com.br`) via Traefik
- The **gateway `bind: loopback` trap** that breaks reverse-proxy access
- Critical OpenClaw networking and provider configuration pitfalls discovered in a live session.

---

## Part 1: Adding Custom Providers (Ollama Cloud + Opencode Go)

OpenClaw's built-in plugin system only supports OpenAI natively. For Ollama Cloud and Opencode, use the `models.providers` JSON section with OpenAI-compatible endpoints.

### Full `models.providers` block (for `openclaw.json`)

```json
"models": {
  "mode": "merge",
  "providers": {
    "ollama": {
      "baseUrl": "https://api.nousresearch.com/v1",
      "apiKey": "<OLLAMA_API_KEY>",
      "auth": "api-key",
      "api": "openai-completions",
      "injectNumCtxForOpenAICompat": false,
      "models": [
        { "id": "kimi-k2.6", "name": "kimi-k2.6", "supportsStreaming": true },
        { "id": "deepseek-v4-pro", "name": "deepseek-v4-pro", "supportsStreaming": true },
        { "id": "deepseek-v4-flash", "name": "deepseek-v4-flash", "supportsStreaming": true },
        { "id": "glm-5.1", "name": "glm-5.1", "supportsStreaming": true },
        { "id": "gemma4:31b", "name": "gemma4:31b", "supportsStreaming": true },
        { "id": "minimax-m2.7", "name": "minimax-m2.7", "supportsStreaming": true }
      ]
    },
    "opencode-go": {
      "baseUrl": "https://opencode.ai/zen/go/v1",
      "apiKey": "<OPENAI_API_KEY>",
      "auth": "api-key",
      "api": "openai-completions",
      "injectNumCtxForOpenAICompat": false,
      "models": [
        { "id": "kimi-k2.6", "name": "kimi-k2.6", "supportsStreaming": true },
        { "id": "deepseek-v4-pro", "name": "deepseek-v4-pro", "supportsStreaming": true },
        { "id": "deepseek-v4-flash", "name": "deepseek-v4-flash", "supportsStreaming": true },
        { "id": "glm-5.1", "name": "glm-5.1", "supportsStreaming": true },
        { "id": "minimax-m2.7", "name": "minimax-m2.7", "supportsStreaming": true },
        { "id": "mimo-v2-pro", "name": "mimo-v2-pro", "supportsStreaming": true },
        { "id": "qwen3.6-plus", "name": "qwen3.6-plus", "supportsStreaming": true }
      ]
    }
  }
}
```

### Adding aliases

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "ollama/kimi-k2.6",
      "fallbacks": [
        "ollama/deepseek-v4-pro",
        "ollama/glm-5.1",
        "opencode-go/kimi-k2.6"
      ]
    },
    "models": {
      "ollama/kimi-k2.6": { "alias": "Ollama Cloud Kimi K2.6" },
      "ollama/deepseek-v4-pro": { "alias": "Ollama Cloud DeepSeek V4 Pro" },
      "ollama/deepseek-v4-flash": { "alias": "Ollama Cloud DeepSeek V4 Flash" },
      "ollama/glm-5.1": { "alias": "Ollama Cloud GLM 5.1" },
      "ollama/gemma4:31b": { "alias": "Ollama Cloud Gemma 4 31B" },
      "ollama/minimax-m2.7": { "alias": "Ollama Cloud MiniMax M2.7" },
      "opencode-go/kimi-k2.6": { "alias": "Opencode Go Kimi K2.6" },
      "opencode-go/deepseek-v4-pro": { "alias": "Opencode Go DeepSeek V4 Pro" },
      "opencode-go/deepseek-v4-flash": { "alias": "Opencode Go DeepSeek V4 Flash" },
      "opencode-go/glm-5.1": { "alias": "Opencode Go GLM 5.1" },
      "opencode-go/minimax-m2.7": { "alias": "Opencode Go MiniMax M2.7" },
      "opencode-go/mimo-v2-pro": { "alias": "Opencode Go Mimo V2 Pro" },
      "opencode-go/qwen3.6-plus": { "alias": "Opencode Go Qwen 3.6 Plus" }
    }
  }
}
```

### Critical Pitfalls

1. **`apiKeyEnv` is NOT valid** — The schema rejects it. Use `apiKey` with the literal key, or set it on the container as an env var and reference differently. Do NOT write `apiKeyEnv`.
2. **Use internal IDs, not aliases, for `primary` and `fallbacks`** — Hostinger's `/hostinger/server.mjs` intercepts config load and rewrites `primary` to a default model ID if it detects an alias. Using `ollama/kimi-k2.6` (internal ID) prevents this silent overwrite.
3. **Container env vars required** — `OLLAMA_API_KEY` and `OPENAI_API_KEY` must be set on the container so the providers can authenticate.

---

## Part 2: Custom Domain via Traefik

### The Problem

OpenClaw's container comes with `--network host` in the Hostinger panel default. The gateway binds to `loopback` by default (`127.0.0.1`), which means:
- Traefik (in `proxy` network) **cannot reach** the gateway via Docker DNS
- Even with port mapping, Traefik sees no listening socket on the shared network

Result: **504 Gateway Timeout** from Traefik to OpenClaw.

### Solution (Non-Destructive)

Recreate the container on the `proxy` network with `bind: lan` in the gateway config and Traefik labels.

#### Step 1: Locate existing container details
```bash
docker inspect openclaw-4vbk-openclaw-1 --format '{{json .HostConfig}}' | python3 -m json.tool | head -40
# Note: Image, Env, Labels, Volumes, RestartPolicy
```

#### Step 2: Backup config before any change
```bash
docker exec openclaw-4vbk-openclaw-1 cat /data/.openclaw/openclaw.json > /opt/data/openclaw-config-backup-$(date +%Y%m%d_%H%M%S).json
```

#### Step 3: Stop and remove old container
```bash
docker stop openclaw-4vbk-openclaw-1
docker rm openclaw-4vbk-openclaw-1
```

#### Step 4: Recreate on `proxy` network with Traefik labels

The `docker run` command must preserve ALL original configuration (image, env vars, volume mounts) except changing `--network` and adding Traefik labels.

```bash
docker run -d \
  --name openclaw-4vbk-openclaw-1 \
  --network proxy \
  --restart unless-stopped \
  -p 127.0.0.1:64551:64551/tcp \
  -v /opt/data/home/openclaw-data:/data:rw \
  -e OPENAI_API_KEY='<REDACTED>' \
  -e OLLAMA_API_KEY='<REDACTED>' \
  -e OPENCLAW_GATEWAY_TOKEN='<REDACTED>' \
  -e HERMES_GATEWAY_TOKEN='<REDACTED>' \
  -e NEXOS_GATEWAY_TOKEN='<REDACTED>' \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=proxy" \
  -l "traefik.http.routers.openclaw-somosflux.entrypoints=websecure" \
  -l "traefik.http.routers.openclaw-somosflux.rule=Host(\`openclaw.somosflux.com.br\`)" \
  -l "traefik.http.routers.openclaw-somosflux.tls.certresolver=default" \
  -l "traefik.http.routers.openclaw-somosflux.service=openclaw-somosflux" \
  -l "traefik.http.services.openclaw-somosflux.loadbalancer.server.port=64551" \
  ghcr.io/hostinger/hvps-openclaw:latest
```

**Key changes from original:**
- `--network proxy` instead of `--network host` (or default)
- `-p 127.0.0.1:64551:64551/tcp` to bind only localhost (Traefik reaches via Docker IP on `proxy` network)
- `-v /opt/data/home/openclaw-data:/data:rw` — adjust to match actual host path
- All original env vars preserved (especially API keys and gateway tokens)
- Traefik labels added for automatic TLS certificate and routing

#### Step 5: Rewrite gateway config for `bind: lan`

```bash
docker exec openclaw-4vbk-openclaw-1 python3 << 'PYEOF'
import json, sys

path = '/data/.openclaw/openclaw.json'
with open(path, 'r') as f:
    config = json.load(f)

# Change gateway bind from loopback to lan (0.0.0.0)
config.setdefault('gateway', {})
config['gateway']['bind'] = 'lan'
config['gateway']['port'] = 64551
config['gateway']['mode'] = 'local'

# Add allowed origins for the custom domain
config['gateway'].setdefault('controlUi', {})
origins = config['gateway']['controlUi'].setdefault('allowedOrigins', [])
for o in ['https://openclaw.somosflux.com.br', 'https://somosflux.com.br']:
    if o not in origins:
        origins.append(o)

with open(path, 'w') as f:
    json.dump(config, f, indent=2)

print('Gateway config updated.')
print('  bind:', config['gateway'].get('bind'))
print('  port:', config['gateway'].get('port'))
print('  origins:', config['gateway']['controlUi']['allowedOrigins'])
PYEOF
```

#### Step 6: Restart container to pick up config
```bash
docker restart openclaw-4vbk-openclaw-1
```

#### Step 7: Verify external access
```bash
curl -s -o /dev/null -w "%{http_code}" "https://openclaw.somosflux.com.br/chat?session=main"
# Expected: 200
```

---

## Summary of Critical Pitfalls Discovered

| # | Pitfall | Impact | Fix |
|---|---------|--------|-----|
| 1 | Gateway defaults to `bind: loopback` (`127.0.0.1`) | Traefik gets 504 / connection refused | Set `bind: lan` → listens on `0.0.0.0` |
| 2 | Container on `--network host` | Traefik cannot resolve container via Docker DNS | Move to shared bridge network (`proxy`) |
| 3 | `apiKeyEnv` in `models.providers` | Config rejected; provider fails to load | Use `apiKey` with literal value |
| 4 | `primary` model set to alias string | Hostinger `server.mjs` silently overwrites to default | Use internal ID (`provider/model-id`) |
| 5 | Port mapping `0.0.0.0:PORT` without gateway `lan` | External port works, internal proxy network fails | Bind both: `--network proxy` + `-p 127.0.0.1:PORT` + `bind: lan` |
| 6 | Missing `allowedOrigins` | CORS preflight blocked on custom domain | Add domain to `gateway.controlUi.allowedOrigins` |
| 7 | Managed panel recreates container | All runtime changes lost | Always recreate using `docker run` with full config, or use File Provider for routing |

---

## Provider Model Mapping Quick Reference

| Provider | Base URL | Model Prefix | Auth String | API Key Env Var | Session Verified |
|---|---|---|---|---|---|
| Ollama Cloud | `https://api.nousresearch.com/v1` | `ollama/` | `api-key` | `OLLAMA_API_KEY` | ✅ 2026-05-09 |
| Opencode Go | `https://opencode.ai/zen/go/v1` | `opencode-go/` | `api-key` | `OPENAI_API_KEY` | ✅ 2026-05-09 |
| OpenAI | `https://api.openai.com/v1` | `openai/` | built-in | `OPENAI_API_KEY` | ✅ (default) |

---

## Files referenced in session

- `/data/.openclaw/openclaw.json` (inside container) — active config
- `/opt/data/home/openclaw-data` (host) — volume for persisting config/data
- `/opt/data/openclaw-config-backup-<timestamp>.json` — backup taken before change
- `/opt/data/openclaw-config-FINAL-20260509.json` — final working config backup
