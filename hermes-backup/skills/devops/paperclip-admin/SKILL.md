---
name: paperclip-admin
category: devops
description: Administer and troubleshoot Paperclip — the paperless document management system. Covers auth debugging, password reset via database, env var precedence, config.json internals, and origin/hostname diagnostics.
triggers:
  - Paperclip login fails with "invalid username or password" or "Invalid origin"
  - Need to reset Paperclip admin password
  - Paperclip rejecting requests from a custom domain
  - Paperclip env vars vs config.json confusion
  - Diagnosing Paperclip auth issues via logs or database
---

# Paperclip Administration & Troubleshooting

## Quick Reference

- **Container image:** `ghcr.io/hostinger/hvps-paperclip:latest`
- **Internal port:** `3100`
- **Auth system:** Better Auth (v1.4.18) with scrypt password hashing
- **Database:** Embedded PostgreSQL on port `54329`
- **Config file:** `/paperclip/instances/default/config.json`
- **Data directory (mounted):** `/docker/paperclip-XXXX/data` → `/paperclip`
- **CLI:** `/usr/local/bin/paperclipai`
- **Server dist:** `/usr/local/lib/node_modules/paperclipai/dist/index.js`

## Auth System Overview

Paperclip uses **Better Auth** for authentication. Key internals:

- **Password hashing:** scrypt with N=16384, r=16, p=1, dkLen=64
- **Hash format:** `salt:key` (32 hex-char salt + 128 hex-char key)
- **Hash module path:** `/usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/crypto/password.mjs`
- **Database tables:** `user` (user info), `account` (credentials, with `password` and `user_id` columns)

## Diagnosis: Login Failing

### Step 1: Check Paperclip logs for auth errors

```bash
docker logs paperclip-tjjz-paperclip-1 --tail 100 2>&1 | grep -i -E "auth|login|origin|403|401"
```

Key patterns:
- `ERROR [Better Auth]: Invalid origin: https://domain.com` → **Origin blocked** (403). The domain is not in `PAPERCLIP_PUBLIC_URL` or `BETTER_AUTH_TRUSTED_ORIGINS`.
- `POST /api/auth/sign-in/email 401` → **Invalid credentials** (401). Password is wrong or user doesn't exist.
- `POST /api/auth/sign-in/email 403` → **Origin rejected** (403). Request blocked before credential validation.

### Step 2: Check env vars

```bash
docker inspect paperclip-tjjz-paperclip-1 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -i paperclip
```

Critical env vars:
- `PAPERCLIP_PUBLIC_URL` — determines the trusted origin for Better Auth
- `PAPERCLIP_ALLOWED_HOSTNAMES` — additional allowed hostnames
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` — bootstrap credentials (only used on first run)

### Step 3: Check config.json

```bash
docker exec paperclip-tjjz-paperclip-1 cat /paperclip/instances/default/config.json
```

Key fields:
- `auth.publicBaseUrl` — used when `baseUrlMode === "explicit"` but **only if env var is NOT set**
- `auth.baseUrlMode` — `"explicit"` or `"auto"`
- `server.allowedHostnames` — Express-level hostname allowlist (separate from Better Auth origins)

## Env Var Precedence (Critical Pitfall)

**`PAPERCLIP_PUBLIC_URL` env var takes ABSOLUTE PRECEDENCE over `config.json`'s `auth.publicBaseUrl`.**

The `resolveBaseUrl()` function (in the Paperclip server dist) checks in this order:
1. `explicitBaseUrl` parameter (passed directly to function)
2. `process.env.PAPERCLIP_PUBLIC_URL`
3. `process.env.PAPERCLIP_AUTH_PUBLIC_BASE_URL`
4. `process.env.BETTER_AUTH_URL`
5. `process.env.BETTER_AUTH_BASE_URL`
6. `config.json` → `auth.publicBaseUrl` (only if `baseUrlMode === "explicit"`)
7. Constructed from `host:port`

This means: if the Docker container was created with `PAPERCLIP_PUBLIC_URL=http://old-hostinger-url.com`, updating config.json's `auth.publicBaseUrl` to the custom domain **has no effect**. The env var wins.

The same applies to `PAPERCLIP_ALLOWED_HOSTNAMES`. The runtime config merges env var values with the publicUrl hostname, but **does NOT read config.json's allowedHostnames**.

### How runtime config is built

```js
allowedHostnamesFromEnv = PAPERCLIP_ALLOWED_HOSTNAMES.split(",")
hostnameFromPublicUrl = new URL(publicUrl).hostname
→ allowedHostnames = [...allowedHostnamesFromEnv, hostnameFromPublicUrl]
```

The config.json `server.allowedHostnames` is NOT consulted at runtime — only used during `paperclipai onboard` bootstrap.

### Fix: Update env vars via panel

To add a custom domain, update these env vars in the Hostinger panel (or Docker run command) and recreate the container:

```
PAPERCLIP_PUBLIC_URL=https://custom.domain.com
PAPERCLIP_ALLOWED_HOSTNAMES=custom.domain.com,original.hostinger.cloud
```

## Password Reset via Database

When the admin password is lost and login is blocked, reset via the embedded PostgreSQL.

### Step 1: Connect to the database

The `pg` module is available inside the container at:
```
/usr/local/lib/node_modules/paperclipai/node_modules/pg
```

### Step 2: Use the Better Auth hashPassword function

```bash
docker exec <container> node -e "
const { Pool } = require('/usr/local/lib/node_modules/paperclipai/node_modules/pg');
const { hashPassword } = require('/usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/crypto/password.mjs');

async function main() {
  const newPassword = 'NewPassword123!';
  const hash = await hashPassword(newPassword);
  
  const pool = new Pool({
    host: 'localhost', port: 54329, database: 'paperclip', user: 'paperclip', password: 'paperclip'
  });
  
  const result = await pool.query(
    \"UPDATE account SET password = \\\$1, updated_at = NOW() WHERE provider_id = 'credential'\",
    [hash]
  );
  console.log('Rows updated:', result.rowCount);
  
  await pool.end();
}
main().catch(e => console.error('Error:', e));
"
```

### Step 3: Verify the new password works

```bash
docker exec <container> curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"email":"user@email.com","password":"NewPassword123!"}'
```

Expected response: `{"redirect":false,"token":"...","user":{...}}`

### Step 4: Verify user exists in database

```bash
docker exec <container> node -e "
const { Pool } = require('/usr/local/lib/node_modules/paperclipai/node_modules/pg');
const pool = new Pool({ host: 'localhost', port: 54329, database: 'paperclip', user: 'paperclip', password: 'paperclip' });
(async () => {
  const users = await pool.query('SELECT id, name, email FROM \"user\"');
  console.log('Users:', JSON.stringify(users.rows, null, 2));
  await pool.end();
})();
"
```

## Bypassing Origin Check (Temporary Workarounds)

When the env vars can't be changed immediately (e.g. Hostinger panel update pending), use these workarounds ranked by impact:

### 1. Code Patch: Disable Origin Check Entirely (best for web UI access)

Patch the Better Auth context to always skip origin validation:

```bash
# Find and patch skipOriginCheck in create-context.mjs
docker exec <container> sudo sed -i \
  's/skipOriginCheck: options.advanced?.disableOriginCheck !== void 0 ? options.advanced.disableOriginCheck : isTest() ? true : false,/skipOriginCheck: true,/' \
  /usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/context/create-context.mjs

# Verify
docker exec <container> grep "skipOriginCheck" /usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/context/create-context.mjs
# Expected: skipOriginCheck: true,
```

**Pitfall:** `sed -i` fails with "Permission denied" because node_modules is owned by root. Use `sudo sed` inside the container.

After patching, restart the paperclip process (see [Restarting Paperclip Process](#restarting-paperclip-process-inside-container)).

### 2. Test via Docker Network (bypass origin for API testing)

Test credentials by sending requests from inside the container with a trusted origin:

```bash
docker exec <container> curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"email":"user@email.com","password":"pass"}'
```

### 3. Set BETTER_AUTH_TRUSTED_ORIGINS at Container Creation

Add `BETTER_AUTH_TRUSTED_ORIGINS=https://custom.domain.com` as a Docker env var. This is read by Better Auth at startup and merged into the trusted origins list.

## Restarting Paperclip Process Inside Container

The Paperclip container does NOT have `pgrep`, `ps`, or `killall`. Use these methods:

### Find the process PID

```bash
docker exec <container> cat /proc/*/status | grep -E "Name:|Pid:" | head -20
```

Look for `MainThread` (the Node.js paperclip process). The entrypoint.sh is PID 1.

### Restart (kill to trigger auto-restart)

The entrypoint script (`/entrypoint.sh`) runs as PID 1 and spawns the paperclip process. Killing the MainThread causes the container to restart the process via entrypoint:

```bash
# Kill MainThread (find its PID from /proc/*/status first)
docker exec <container> sh -c 'kill -9 <MAINTHREAD_PID>'

# Wait for restart and verify
sleep 5
docker exec <container> sh -c 'cat /proc/*/status | grep -E "Name:|Pid:" | head -20'
```

**Note:** This only restarts the Node process — Docker env vars remain unchanged. Code patches to `node_modules` persist until container recreation.

## Paperclip API Interaction

The Paperclip API is a JSON REST API. Key patterns for programmatic access:

### Authentication

Uses cookie-based sessions (not Bearer tokens). The login endpoint sets `paperclip-default.session_token` cookie.

```bash
COOKIE_JAR=$(mktemp)
curl -s -c "$COOKIE_JAR" -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"email":"user@email.com","password":"pass"}' > /dev/null

# All subsequent calls use the cookie jar
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/agents/ceo?companyId=<companyId>"
```

### API Prefix

- `/api/` prefix returns **JSON** responses
- Routes WITHOUT `/api/` prefix return the **React SPA HTML** (for browser navigation)
- Always add `-H "Accept: application/json"` for reliable JSON responses

### Common Endpoints

| Endpoint | Description |
|---|---|
| `POST /api/auth/sign-in/email` | Login, returns `{token, user}` |
| `GET /api/auth/get-session` | Check current session |
| `GET /api/agents/:id?companyId=X` | Get agent details |
| `GET /api/agents/:id/runtime-state?companyId=X` | Agent runtime state (last run, errors, session) |
| `GET /api/agents/:id/config-revisions?companyId=X` | Config change history |
| `GET /api/companies/:id/agents` | List all agents in company |
| `GET /api/companies/:id/secrets` | Company secrets (API keys, etc.) |
| `GET /api/companies/:id/adapters/:type/detect-model` | Detect available models for adapter |
- `references/agent-config-and-tasking.md` — Agent API patterns: config PATCH, heartbeat enabling, issue creation, execution flow
- `references/model-audit.md` — Cross-service model audit: Hermes + Paperclip + OpenClaw, reconcile against available models

## Agent Troubleshooting

### hermes_local Adapter

The `hermes_local` adapter connects Paperclip agents to a local Hermes Agent instance. It requires:

| Config Field | Required | Description |
|---|---|---|
| `mode` | **YES** | Must be non-empty (likely `"hermes"` or similar) |
| `model` | **YES** | Model name (e.g., `"deepseek-v4-pro"`) |
| `effort` | No | Reasoning effort level |
| `timeoutSec` | No | Timeout in seconds (0 = no timeout) |
| `graceSec` | No | Grace period (default 15) |
| `instructionsFilePath` | No | Path to AGENTS.md instructions |

### "Process adapter missing command" Error

When an agent's `adapterType` shows as `hermes_local` in the agent list but `process` in the runtime state, and `lastError` is `"Process adapter missing command"`, the Hermes CLI binary is not installed inside the Paperclip container. The `hermes_local` adapter spawns `hermes chat -q "..."` as a child process. If `hermes` is not on the container's PATH, the adapter falls back to a generic `process` adapter and fails.

**Fix:** Install the Hermes CLI inside the Paperclip container. See `references/hermes-local-adapter-setup.md` for the full workflow.

### 401 Errors on Agent Heartbeat / API Calls

If logs show a steady stream of `401` responses on `/api/companies/:id/issues`, `/api/auth/get-session`, or agent REST endpoints, the root cause is almost always **origin mismatch** between `PAPERCLIP_PUBLIC_URL` (env var) and the actual domain used by clients.

The `PAPERCLIP_PUBLIC_URL` env var takes **absolute precedence** over `config.json`'s `auth.publicBaseUrl`. If `PAPERCLIP_PUBLIC_URL=http://old-hostinger-url.cloud` but agents and browsers access via `https://custom.domain.com.br`, Better Auth will reject every authenticated request with 401 because the origin doesn't match.

**Diagnosis:**
```bash
# Check what origin the server thinks is authoritative
docker inspect <container> --format '{{range .Config.Env}}{{println .}}{{end}}' | grep PAPERCLIP_PUBLIC_URL
# Compare with config.json
docker exec <container> cat /paperclip/instances/default/config.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('auth',{}).get('publicBaseUrl','NOT SET'))"
```

**Quick fix (no container recreation):** Patch Better Auth to skip origin validation:
```bash
docker exec <container> sudo sed -i \
  's/skipOriginCheck: options.advanced?.disableOriginCheck !== void 0 ? options.advanced.disableOriginCheck : isTest() ? true : false,/skipOriginCheck: true,/' \
  /usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/context/create-context.mjs
# Then restart the Paperclip process (not the container)
```

**Proper fix:** Recreate the container with corrected env vars:
```
PAPERCLIP_PUBLIC_URL=https://custom.domain.com.br
PAPERCLIP_ALLOWED_HOSTNAMES=custom.domain.com.br,old-hostinger.cloud
```

### ADMIN_PASSWORD env var doesn't work (only used on first boot)

The `ADMIN_PASSWORD` environment variable is only read during the **first bootstrap** when no admin user exists. If the admin user was already created (even on a previous container start), changing the env var has no effect. The password must be reset via the database.

### Pitfall: Individual Agent Endpoint Requires Full UUID

When querying `GET /api/agents/:id?companyId=X`, you **must** use the full 36-character UUID (e.g., `763e73f1-326c-4ba1-8c72-2b860a26e4c1`). Using a truncated 16-char prefix returns empty/error responses silently — `name`, `role`, `adapterConfig` all come back as empty strings. This is especially confusing because the **list endpoint** `GET /api/companies/:id/agents` returns truncated IDs in its display, but the full ID in the `id` field.

**Safe pattern:** Always extract the full `id` from the list endpoint response before querying individual agents. Never substring it.

### Common Agent Errors

**`status: "error"` with `lastRunStatus: "failed"` and `error: "Adapter failed"`:**
- Check if `mode` and `model` are empty in `adapterConfig`
- Run `detect-model` endpoint — if it returns `null`, Hermes isn't reachable
- Check company secrets for any required API keys
- Verify the instructions file exists at `instructionsFilePath`

**`detect-model` returns `null`:**
- The adapter can't reach the Hermes Agent CLI or API
- Check that `hermes` is installed and accessible in the container
- Or the Hermes Agent endpoint may need to be configured

### Checking Agent State

```bash
# Get agent info including error status
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/agents/<agentId>?companyId=<companyId>"

# Get runtime state (last run, error details, session params)
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/agents/<agentId>/runtime-state?companyId=<companyId>"

# Get config revision history (to see what changed)
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/agents/<agentId>/config-revisions?companyId=<companyId>"
```

## Hermes Agent Infrastructure (VPS Context)

Paperclip runs on a Hostinger VPS alongside Hermes Agent. Key infrastructure facts that affect Paperclip:

- **VPS**: 4 vCPU, 7.7GB RAM, 4GB swap (created via `fallocate -l 4G /swapfile`)
- **Memory limits**: Hermes 3GB, OpenClaw 2GB, Paperclip 1GB, WebUI 512MB, Traefik 256MB
- **Pitfall**: `docker update --memory` limits are lost when containers are recreated (e.g. Hostinger "Atualizar" button). Re-apply after recreation.
- **OpenClaw DNS**: `api.nousresearch.com` is dead. Config must point to `opencode.ai/zen/go/v1`.
- **Hermes fallback providers**: `glm-5.1` and `kimi-k2.6` via opencode-go
- **Hermes checkpoints**: enabled (max 20 snapshots, 7-day retention)
- **Hermes delegation depth**: 2 (subagents can create sub-subagents)
- **Backup**: Daily at 03:00 UTC via cron job `flux-vps-backup`, script at `/opt/data/scripts/backup-vps.sh`
- **Hermes CLI inside Paperclip**: Installed via apt → copy venv → copy modules → symlink → chown. Required for hermes_local adapter.

## Hermes CLI Installation Inside Paperclip Container

The `hermes_local` adapter spawns `hermes chat -q "..."` as a child process. If Hermes is not installed inside the Paperclip container, agents stay in `status: "error"` with `"Adapter failed"`. See the full step-by-step guide:

→ `references/hermes-local-adapter-setup.md` — Python + venv copy + config setup + API key configuration

Quick summary of the workflow:
1. Install Python 3 + pip via apt (as root)
2. Copy Hermes venv from host (`/opt/hermes/.venv/`)
3. Copy Python modules (`hermes_cli/`, `agent/`, `providers/`, etc.)
4. Fix entry point symlink to use venv Python
5. Copy config and `.env` to container HOME (`/paperclip/.hermes/`)
6. Fix permissions (docker cp preserves UID/GID → chown needed)
7. Add API keys to agent's `adapterConfig.env` if `.env` file has issues

## Agent Configuration & Tasking

→ `references/agent-config-and-tasking.md` — PATCH patterns, heartbeat enabling, issue creation, execution flow

Key patterns:
- PATCH agent adapterConfig: requires `Origin` header even after origin bypass
- Include ALL adapterConfig fields in PATCH, not just changed fields (omit = clear)
- Enable heartbeat: `runtimeConfig.heartbeat.enabled = true`
- Create issues for agents: `POST /api/companies/{id}/issues` with `assigneeAgentId`
- `env` field in adapterConfig passes environment variables to spawned Hermes process

## Agent Model Standardization

When assigning models to Paperclip agents, prioritize by task complexity and cost:

- **deepseek-v4-pro** → Strategic roles (CEO, CFO, CTO, dir-ghl) — complex reasoning, multi-step decisions
- **glm-5.1** → Operational roles (CMO, operations-director) — content generation, routine tasks, cheaper
- **kimi-k2.6** → Sales/reasoning roles (sales-director) — qualification logic, conversation reasoning

Use PATCH `/api/agents/:id?companyId=:companyId` with the **full** `adapterConfig` object (partial PATCH clears omitted fields). Always include `instructionsFilePath` and `env` with `OPENCODE_GO_API_KEY`.

## VPS Backup Automation

Daily backup via Hermes cron job (`flux-vps-backup`) at 03:00 UTC:
- Paperclip PostgreSQL dump (pg_dump → gzip)
- Hermes config.yaml + .env
- OpenClaw openclaw.json
- Docker container inspect specs (for recreation)
- 7-day retention, stored in `/opt/data/backups/`

Script: `/opt/data/scripts/backup-vps.sh`

**Pitfall:** `docker update --memory` limits are lost when containers are recreated (e.g. Hostinger "Atualizar" button). Re-apply after recreation.

## Related Skills

- `docker-traefik-routing` — For Traefik/proxy/network issues affecting Paperclip routing
- `hermes-agent` — For Hermes Agent configuration (often deployed alongside Paperclip)

## References

- `references/auth-debugging-session-2026-05-09.md` — Full debugging transcript: origin rejection, password reset via scrypt hash, env var precedence discovery
- `references/auth-debugging-vps-audit-2026-05-09.md` — VPS-wide audit session: PAPERCLIP_PUBLIC_URL mismatch causing 126x 401 errors, password drift, CTO agent error
- `references/vps-infrastructure-audit.md` — Full VPS infrastructure audit: swap, memory limits, Docker cleanup, OpenClaw DNS fix, backup automation, Hermes CLI install inside Paperclip, agent model standardization
- `references/paperclip-api-commands.md` — API interaction patterns: auth flow, common endpoints, agent troubleshooting, and hermes_local adapter config
- `references/hermes-local-adapter-setup.md` — Complete workflow: installing Hermes CLI inside Paperclip container for the hermes_local adapter
- `references/agent-config-and-tasking.md` — Agent API patterns: config PATCH, heartbeat enabling, issue creation, execution flow
