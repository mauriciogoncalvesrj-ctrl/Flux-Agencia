---
name: openclaw
description: "Deploy, configure, and maintain OpenClaw — the autonomous AI agent CLI by Hostinger — especially in Docker and Hostinger VPS environments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [openclaw, ai-agent, cli, docker, hostinger, vps, configuration, providers]
    homepage: https://github.com/openclaw/openclaw
    related_skills: [hermes-agent, claude-code, codex, opencode]
---

# OpenClaw

OpenClaw is an autonomous AI agent CLI (similar to Hermes Agent, Claude Code, Codex, and OpenCode) developed by Hostinger. It runs as a Docker container in the Hostinger VPS Docker Compose Catalog and provides a web-based control UI, gateway, and agent loop.

**This skill covers OpenClaw operations** — version checks, configuration, provider setup, and Docker-level maintenance — with a focus on the Hostinger managed-panel deployment model.

---

## Quick Facts

- **Container image:** `ghcr.io/hostinger/hvps-openclaw:latest`
- **Container name pattern:** `openclaw-<hash>-openclaw-1`
- **Main process:** `node server.mjs`
- **Sub-processes:** `openclaw`, `openclaw-gateway`
- **Config file (inside container):** `/data/.openclaw/openclaw.json`
- **Data volume (host):** docs say `/docker/openclaw-<hash>/data`, but Hostinger often uses managed Docker volumes invisible on the host. Verify with `docker inspect <container> --format '{{json .HostConfig.Binds}}'`.
- **Gateway port:** dynamically assigned by the panel (e.g., `64551`). Discover with `docker port <container>` or read from `openclaw.json`.
- **Default network:** often `host` in panel deployments; must be moved to a Docker bridge network (e.g., `proxy`) for Traefik routing.
- **Default webchat client version:** reported in gateway logs as `openclaw-control-ui webchat vYYYY.M.DD`

---

## Version Management

### Check installed version
```bash
docker exec <container> openclaw --version
```
Example output: `OpenClaw 2026.4.21 (f788c88)`

### Check latest release (GitHub)
```bash
curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" | grep '"tag_name"'
```
The repository is `openclaw/openclaw` on GitHub. If the API returns 404, try checking the releases page directly: `https://github.com/openclaw/openclaw/releases`.

### In-Container npm Update (Advanced)
If the Docker image is stale but a newer OpenClaw CLI is available via npm, you can update **inside the running container** without waiting for a new image. This is useful when:
- The Hostinger panel image hasn't been rebuilt yet.
- You need the newest release immediately.

#### Workflow
1. **Backup config:**
   ```bash
   docker exec <container> cat /data/.openclaw/openclaw.json > /opt/data/openclaw-config-backup.json
   ```

2. **Dry-run to preview:**
   ```bash
   docker exec <container> openclaw update --dry-run --json --yes
   ```

3. **Apply the update (run as container's user):**
   ```bash
   docker exec <container> openclaw update --yes --no-restart --json
   ```
   This downloads the latest npm package and installs it under `/data/.npm-global/lib/node_modules/openclaw`.

4. **Restart the container** so the new binary is picked up:
   ```bash
   docker restart <container>
   ```
   > **Note:** `--no-restart` tells the OpenClaw CLI not to restart its own gateway process, but the container itself still needs a Docker-level restart because the Docker image layer still points to the old binary. The `entrypoint.sh` (which runs as root before dropping to the `node` user) does not pick up the `.npm-global/bin` path change until the container restarts.

5. **Verify:**
   ```bash
   docker exec <container> openclaw --version
   docker exec <container> openclaw health
   ```

#### Pitfalls
- **Old binary persists until container restart:** After `openclaw update` completes, `which openclaw` inside the container may still point to the Docker image layer (`/usr/local/bin/openclaw` → old version). A `docker restart` is required for the new path (`/data/.npm-global/bin/openclaw`) to become effective.
- **Run as correct user:** The `openclaw update` command writes to `/data/.npm-global/` (user-writable). Do not run it as root inside the container unless you update the system path afterward. The Hostinger container defaults run as the `node` user for this reason.
- **Gateway process mismatch:** If you skip the container restart, the *running* `openclaw-gateway` process may still be the old version even though the CLI binary is new.

### Update the container (Panel Method)
On Hostinger managed panels, use the **"Atualizar" (Update)** button in the panel. This pulls the latest image and recreates the container. Any runtime changes (like manual network attachments) will be lost — this is expected behavior for managed Docker Compose.

---

## Configuration (`openclaw.json`)

The master config lives at `/data/.openclaw/openclaw.json` inside the container. It persists across container recreations because `/data` is a host-mounted volume.

### Read the config
```bash
docker exec <container> cat /data/.openclaw/openclaw.json | python3 -m json.tool
```

### Key sections

| Section | Purpose |
|---------|---------|
| `update` | Update channel (`stable`) and check-on-start behavior |
| `browser` | Headless browser settings (`headless: true`, `noSandbox: true`) |
| `commands` | Toggle bash/native/restart permissions |
| `tools` | Tool profile (`full`), elevated permissions |
| `agents` | Agent list, default workspace, default model, model aliases |
| `gateway` | Local mode, auth token, rate limits, allowed origins |
| `plugins` | Enabled plugins (`browser`, `openai`, etc.) |
| `skills` | Extra skill dirs and per-skill toggles |
| `models` | Model merge mode, custom providers |
| `hooks` | Webhook token |
| `meta` | Last touched timestamp and version |

### Default model & fallback chain — use internal IDs for persistence

The `agents.defaults.model.primary` field sets the default model. Use the **internal ID** (e.g., `ollama/kimi-k2.6`) rather than an alias (e.g., "Ollama Cloud Kimi K2.6").

**Why:** Hostinger's `/hostinger/server.mjs` intercepts config load and rewrites the `primary` field (and fallbacks) to use default model IDs if it detects an alias in those slots. This silently overwrites your desired configuration. Using internal IDs bypasses this enforcement.

```json
"model": {
  "primary": "ollama/kimi-k2.6",
  "fallbacks": [
    "ollama/deepseek-v4-pro",
    "ollama/glm-5.1",
    "opencode-go/kimi-k2.6"
  ]
}
```

**Pitfall:** Setting `"primary": "Ollama Cloud Kimi K2.6"` (alias) will cause the Hostinger server script to reset it to the built-in Nexos default model on startup. (Custom Endpoints via `models.providers`)

OpenClaw supports custom OpenAI-compatible endpoints through the **`models.providers`** section. This is the correct way to add Ollama Cloud, Opencode Go, OpenRouter, or any other provider with a custom `baseUrl`.

1. Add a provider block under **`models.providers.<providerId>`**:
   ```json
   "ollama": {
     "baseUrl": "https://api.nousresearch.com/v1",
     "apiKey": "<your-api-key>",
     "auth": "api-key",
     "api": "openai-completions",
     "injectNumCtxForOpenAICompat": false,
     "models": [
       { "id": "kimi-k2.6", "name": "kimi-k2.6", "supportsStreaming": true },
       { "id": "deepseek-v4-pro", "name": "deepseek-v4-pro", "supportsStreaming": true }
     ]
   }
   ```

2. Add model aliases under **`agents.defaults.models`** using the internal ID format `<providerId>/<modelId>`:
   ```json
   "ollama/kimi-k2.6": {
     "alias": "Ollama Cloud Kimi K2.6"
   }
   ```

3. Set the corresponding API key as an environment variable on the container (`OLLAMA_API_KEY`, `OPENAI_API_KEY`, etc.).

4. Restart the container for changes to take effect.

**Supported `models.providers.<id>` keys:**
- `baseUrl` (string): Provider API endpoint root
- `apiKey` (string): API key literal. **Do NOT use `apiKeyEnv`** — the schema rejects it.
- `auth` (string): `"api-key"` or `"bearer"`
- `api` (string): `"openai-completions"` for OpenAI-compatible endpoints
- `models` (array): List of model objects with `id`, `name`, `supportsStreaming`, etc.

**Pitfall:** The schema does **not** accept `apiKeyEnv`. Pass the key inline as `apiKey`, or set it via standard container env vars and reference it indirectly — but never use the literal key `apiKeyEnv` in the JSON.

**Pitfall:** Model IDs must match the provider's expected format. OpenRouter uses `openrouter/<vendor>/<model>`; Ollama Cloud uses `ollama/<model>`.

### Programmatic Model Management

When auditing or updating models across providers, use a Python script to read, modify, and write the config — this is safer than manual JSON editing and avoids syntax errors:

```bash
# 1. Extract config from container
docker exec openclaw-<hash>-openclaw-1 cat /data/.openclaw/openclaw.json > /tmp/oc.json

# 2. Modify with Python
python3 -c "
import json
with open('/tmp/oc.json') as f:
    config = json.load(f)

providers = config['models']['providers']
defaults = config['agents']['defaults']

# Remove a model from a provider
ollama_models = providers['ollama']['models']
ollama_models = [m for m in ollama_models if m['id'] != 'gemma4:31b']
providers['ollama']['models'] = ollama_models

# Add new models to a provider
ocg_models = providers['opencode-go']['models']
existing_ids = {m['id'] for m in ocg_models}
new_models = [
    ('glm-5', 'Opencode GLM 5', ['text'], 8192, 200000),
    ('kimi-k2.5', 'Opencode Kimi K2.5', ['text', 'image'], 8192, 200000),
]
for mid, name, inp, mt, cw in new_models:
    if mid not in existing_ids:
        ocg_models.append({'id': mid, 'name': name, 'input': inp, 'maxTokens': mt, 'contextWindow': cw})
providers['opencode-go']['models'] = ocg_models

# Sync agent defaults models dict
models_dict = defaults.get('models', {})
models_dict.pop('ollama/gemma4:31b', None)  # Remove
models_dict['opencode-go/glm-5'] = {'alias': 'Opencode GLM 5'}  # Add

defaults['models'] = models_dict

with open('/tmp/oc_updated.json', 'w') as f:
    json.dump(config, f, indent=2)
"

# 3. Backup original and copy updated config
docker exec openclaw-<hash>-openclaw-1 cp /data/.openclaw/openclaw.json /data/.openclaw/openclaw.json.bak
docker cp /tmp/oc_updated.json openclaw-<hash>-openclaw-1:/data/.openclaw/openclaw.json

# 4. Restart to apply
docker restart openclaw-<hash>-openclaw-1
```

**Key rules:**
- Models must be registered in **both** `models.providers.<id>.models` AND `agents.defaults.models`
- Provider models use `id`, `name`, `input`, `maxTokens`, `contextWindow`
- Agent defaults models use internal ID format `<providerId>/<modelId>` → `{"alias": "Display Name"}`
- Always backup before overwriting (`cp openclaw.json openclaw.json.bak`)

---

## Provider Setup Reference

| Provider | Env Var | Config Section | Model Prefix | Notes |
|----------|---------|----------------|--------------|-------|
| OpenAI | `OPENAI_API_KEY` | `plugins.entries.openai` + built-in | `openai/` | Ships enabled by default |
| OpenRouter | `OPENROUTER_API_KEY` | `models.providers.openrouter` | `openrouter/` | Custom `baseUrl` required |
| Ollama Cloud | `OLLAMA_API_KEY` | `models.providers.ollama` | `ollama/` | ⚠️ See DNS pitfall below |
| Opencode Go | `OPENAI_API_KEY` | `models.providers.opencode-go` | `opencode-go/` | `https://opencode.ai/zen/go/v1` |
| Anthropic | `ANTHROPIC_API_KEY` | `plugins.entries.anthropic` or custom | `anthropic/` | |

For custom providers (Ollama Cloud, Opencode Go, OpenRouter), use the **`models.providers.<id>`** approach with `baseUrl`, `apiKey`, `auth`, `api`, and `models[]`. See `references/openclaw-config-structure.md` for a full annotated example.

See `references/ollama-opencode-provider-config-session.md` for exact recipes from a real configuration session (Ollama Cloud + Opencode Go on 2026-05-09).

---

## Custom Domain via Traefik Reverse Proxy

When exposing OpenClaw on a custom domain (e.g., `https://openclaw.somosflux.com.br/chat?session=main`), two layers must align: **Docker networking** and **application-level gateway binding**.

### The Default Problem

Hostinger panel deployments often place OpenClaw on `--network host` (or a non-shared default). The gateway defaults to `bind: loopback` (`127.0.0.1`). This combination means:
- Traefik cannot reach OpenClaw via Docker DNS
- Even with `-p` port mapping, applications bound to `127.0.0.1` reject connections from the Docker bridge (`172.x.x.x`)
- Result: **504 Gateway Timeout**

### Solution: Three Required Steps

#### 1. Move container to shared Docker network

Recreate (or recreate with explicit `docker run`) on a bridge network that Traefik is also on.

**Preserve all existing config** — env vars, volume mounts, restart policy, port mapping:

```bash
docker run -d \
  --name openclaw-4vbk-openclaw-1 \
  --network proxy \
  --restart unless-stopped \
  -p 127.0.0.1:64551:64551/tcp \
  -v /opt/data/home/openclaw-data:/data:rw \
  -e OPENAI_API_KEY='<key>' \
  -e OLLAMA_API_KEY='<key>' \
  -e OPENCLAW_GATEWAY_TOKEN='<key>' \
  -e HERMES_GATEWAY_TOKEN='<key>' \
  -e NEXOS_GATEWAY_TOKEN='<key>' \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=proxy" \
  -l "traefik.http.routers.openclaw-somosflux.entrypoints=websecure" \
  -l "traefik.http.routers.openclaw-somosflux.rule=Host(\`openclaw.somosflux.com.br\`)" \
  -l "traefik.http.routers.openclaw-somosflux.tls.certresolver=default" \
  -l "traefik.http.routers.openclaw-somosflux.service=openclaw-somosflux" \
  -l "traefik.http.services.openclaw-somosflux.loadbalancer.server.port=64551" \
  ghcr.io/hostinger/hvps-openclaw:latest
```

Key adjustments from default panel deployment:
- `--network proxy` (was `host` or default)
- `-p 127.0.0.1:64551:64551` (bind only localhost, since Traefik reaches via internal Docker IP)
- Traefik labels for automatic TLS and routing
- All original env vars preserved

#### 2. Change application gateway bind from `loopback` to `lan`

The OpenClaw gateway must listen on `0.0.0.0` to accept connections from the Docker bridge:

```json
"gateway": {
  "mode": "local",
  "bind": "lan",
  "port": 64551,
  "controlUi": {
    "allowedOrigins": [
      "http://localhost:18789",
      "http://127.0.0.1:18789",
      "https://openclaw.somosflux.com.br",
      "https://somosflux.com.br"
    ]
  }
}
```

The `lan` value tells OpenClaw to bind to all interfaces (`0.0.0.0`).

**Pitfall:** Without `allowedOrigins`, the browser will block the webchat with CORS errors even when Traefik returns 200. The webchat client runs in the browser and makes direct requests to the gateway.

#### 3. Restart container

```bash
docker restart openclaw-4vbk-openclaw-1
```

#### Verification

```bash
# Check networks
docker inspect openclaw-4vbk-openclaw-1 --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
# Expected: proxy (and possibly others)

# Check what the gateway is bound to
docker exec openclaw-4vbk-openclaw-1 ss -tlnp
# Expected: 0.0.0.0:64551 (or *:64551), NOT 127.0.0.1:64551

# External test
curl -s -o /dev/null -w "%{http_code}" "https://openclaw.somosflux.com.br/chat?session=main"
# Expected: 200
```

---

## Docker-Level Diagnostics

### List OpenClaw containers
```bash
docker ps --filter name=openclaw --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```

### Check running processes
```bash
docker exec <container> ps aux
```
Expected: `docker-init → runuser → node server.mjs → openclaw → openclaw-gateway`

### Check environment variables
```bash
docker exec <container> env | grep -i -E "api_key|provider|model"
```

### Check recent logs
```bash
docker logs --tail 50 <container>
```
Gateway connections are logged with timestamps and client versions.

### Inspect image age
```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}" | grep openclaw
```

---

## Hostinger VPS Specifics

- The panel's **"Atualizar"** button recreates containers from the original compose definition. Runtime changes (network connects, env vars set via `docker exec`) are lost.
- To make persistent changes, modify the compose configuration in the Hostinger panel (environment variables, volume mounts) and then click **"Atualizar"**.
- The OpenClaw data directory on the host is typically `/docker/openclaw-<hash>/data`, mounted to `/data` inside the container.

---

## Troubleshooting

### ⚠️ Ollama Cloud / `api.nousresearch.com` is DEAD (NXDOMAIN)

The domain `api.nousresearch.com` **does not resolve** via any public DNS (confirmed 2026-05-09). If your OpenClaw `models.providers.ollama.baseUrl` points there, every request to provider `ollama/*` will fail with:

```
getaddrinfo ENOTFOUND api.nousresearch.com
```

OpenClaw will then try the fallback chain, adding 20–30s latency before succeeding on the next provider.

**Fix:** Use `https://opencode.ai/zen/go/v1` as the `baseUrl` for the `ollama` provider (same endpoint, different domain). Or remove the `ollama` provider entirely and rely on `opencode-go` which already uses the correct URL.

### ⚠️ Duplicate Provider Causes 404 HTML Error Pages (2026-05-09)

When `ollama` and `opencode-go` providers point to the **same baseUrl** (`https://opencode.ai/zen/go/v1`), the `ollama` provider still prefix-routes models as `ollama/deepseek-v4-pro`, which causes the API to return **404 HTML error pages** instead of JSON responses. This manifests as:

```
FailoverError: The provider returned an HTML error page instead of an API response.
This usually means a CDN or gateway (e.g. Cloudflare) blocked the request.
model-fallback/decision: decision=candidate_failed requested=ollama/deepseek-v4-pro
candidate=ollama/deepseek-v4-pro reason=model_not_found next=ollama/glm-5.1
```

Every request to `ollama/*` models fails, then fallback also fails for `ollama/glm-5.1`, and only succeeds on `opencode-go/kimi-k2.6`. This adds 10-30s latency per request.

**Fix:** Disable the `ollama` plugin entirely and use only `opencode-go` as the provider. Change primary model and all fallbacks to `opencode-go/*` format:

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "opencode-go/kimi-k2.6",
      "fallbacks": [
        "opencode-go/deepseek-v4-pro",
        "opencode-go/glm-5.1",
        "opencode-go/minimax-m2.7"
      ]
    }
  }
}
```

And disable the redundant plugin:
```json
"plugins": { "entries": { "ollama": { "enabled": false } } }
```

### Plugin Validation Failures on Startup

OpenClaw logs which plugins fail validation at startup. Common failures on Hostinger VPS (2026-05-09): `acpx`, `amazon-bedrock`, `amazon-bedrock-mantle`, `browser`, `microsoft`. These appear as:

```
[plugins] 5 plugin(s) failed to initialize (validation: ...)
```

**Fix:** Disable unused plugins in `openclaw.json`:
```json
"plugins": {
  "entries": {
    "openai": { "enabled": true },
    "ollama": { "enabled": true },
    "opencode-go": { "enabled": true },
    "browser": { "enabled": false },
    "acpx": { "enabled": false },
    "amazon-bedrock": { "enabled": false },
    "amazon-bedrock-mantle": { "enabled": false },
    "microsoft": { "enabled": false }
  }
}
```

After editing, restart the container (`docker restart <container>`).

### OpenClaw won't start / gateway not responding
1. Check container status: `docker ps -a | grep openclaw`
2. Check logs: `docker logs <container> --tail 100`
3. Verify `openclaw.json` is valid JSON: `docker exec <container> python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null`
4. **Check for OOM/system resource exhaustion:** If all services go down intermittently (not just OpenClaw), suspect OOM Killer on Hostinger VPS (no swap by default). See `docker-traefik-routing` skill → `references/hostinger-resource-constraints.md` for full diagnosis and swap fix.

### Models not available / "provider not found"
1. Verify the provider plugin is enabled in `openclaw.json`
2. Verify the API key env var is set on the container
3. Verify model IDs match the provider's expected format

### Webchat shows old version after update
- Clear browser cache — the control UI is a web app that may cache assets.
- Verify the container was actually recreated: `docker inspect <container> --format='{{.State.StartedAt}}'`

### Config changes not taking effect
- OpenClaw reads `openclaw.json` at startup. Changes require a container restart (`docker restart <container>` or panel "Atualizar").

### In-Container Update (Simple Method)
The `openclaw update` command can upgrade OpenClaw inside the running container without a Docker image pull.

```bash
# Run update (takes ~50s)
docker exec <container> openclaw update

# Restart to apply
docker restart <container>

# Verify version
docker exec <container> openclaw --version
```

**Pitfall:** After `openclaw update`, the gateway process may be killed (SIGTERM) or become stale. Always `docker restart` afterward.

**Pitfall:** The update command may show warnings like `plugins.entries.acpx: plugin not installed`. These are cosmetic — the plugin was already disabled. Ignore them.

### Telegram Plugin (v2026.5.7+)
As of v2026.5.7, the Telegram plugin **works natively** in the container. Previous versions required native dependencies that were missing, but the current version bundles them. 

**Setup:**
1. Create a Telegram bot via @BotFather and get the token
2. Write the token to `/data/.openclaw/.env`: `TELEGRAM_BOT_TOKEN=<your-token>`
3. Enable the plugin in `openclaw.json`:
   ```json
   "plugins": { "entries": { "telegram": { "enabled": true } } }
   ```
   **Pitfall:** Do NOT add `config: { token: "..." }` inside the telegram entry — the schema rejects additional properties. The token MUST go in the `.env` file.
4. Restart: `docker restart <container>`
5. **Approve the device pairing:** Send any message to the bot on Telegram, then run:
   ```bash
   docker exec <container> openclaw pairing approve telegram <CODE>
   ```
   Find the code in the pairing file: `docker exec <container> cat /data/.openclaw/credentials/telegram-pairing.json`
6. Restart again if needed: `docker restart <container>`

**Verification:** Logs should show `[telegram] starting provider (@botname)` and `[telegram] N commands visible`.

**WhatsApp plugin** still does NOT work — it requires native dependencies not present in the container. Do NOT enable it via WebUI.

### Container Killed (SIGTERM) Unexpectedly
If OpenClaw container stops unexpectedly (logs show `[gateway] signal SIGTERM received`), it was likely killed by an elevated command or manual intervention. Restart with `docker start <container>`.

### ⚠️ Telegram Bot Token in .env + Disabled Plugin → Repeated Crashes
If a `TELEGRAM_BOT_TOKEN` is written to `/data/.openclaw/.env` but the Telegram plugin is disabled or doesn't meet requirements (pre-v2026.5.7), the WebUI may keep trying to activate it, sending `SIGTERM` and crashing the gateway repeatedly.

**Fix:**
1. Clear the `.env` file: `docker exec <container> sh -c 'echo "" > /data/.openclaw/.env'`
2. Ensure plugin config in `openclaw.json` is correct (enabled: true for v2026.5.7+, or removed for older versions)
3. Restart: `docker restart <container>`

### In-Container Update Shows "New Skills Unlocked" (2026.5.7)
After running `openclaw update`, the CLI reports "Leveled up! New skills unlocked." This is normal — the update from 2026.4.21 to 2026.5.7 unlocks new built-in skills. The gateway needs a `docker restart` afterward, and the upgrade logs show `After: 2026.5.7`.

### Post-Update Verification
After any OpenClaw update:
1. `docker restart <container>`
2. Check logs for errors: `docker logs <container> --tail 20 2>&1 | grep -iE "error|fail|FATAL"`
3. Confirm the gateway started: log line `[gateway] ready`
4. Confirm correct model loaded: log line `[gateway] agent model: opencode-go/kimi-k2.6`
5. Check no `ollama/*` 404 errors appear (if ollama provider is disabled, there should be none)

---

## References

- `references/openclaw-config-structure.md` — Annotated example `openclaw.json` with multiple providers (OpenAI, OpenRouter, Ollama Cloud)
