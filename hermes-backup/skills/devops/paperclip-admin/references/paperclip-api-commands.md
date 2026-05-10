# Paperclip API Interaction Patterns

## Auth Flow

Paperclip uses Better Auth with cookie-based sessions. The session cookie is `paperclip-default.session_token`.

```bash
# Login and save cookies
COOKIE_JAR=$(mktemp)
curl -s -c "$COOKIE_JAR" -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"email":"user@email.com","password":"pass"}' > /dev/null

# Check session
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/auth/get-session"

# All subsequent calls use cookie jar
curl -s -b "$COOKIE_JAR" -H "Accept: application/json" \
  "http://localhost:3100/api/<endpoint>"
```

## API Prefix Convention

- `/api/` prefix → JSON response (programmatic access)
- Routes WITHOUT `/api/` → React SPA HTML (browser navigation)
- Always add `-H "Accept: application/json"` for reliable JSON

## Endpoint Catalog

### Authentication
```
POST /api/auth/sign-in/email   → {token, user}
GET  /api/auth/get-session      → session info or 401
```

### Agents
```
GET  /api/agents/:id?companyId=X                → agent details (name, role, status, adapterConfig, errorMessage)
GET  /api/agents/:id/runtime-state?companyId=X  → runtime state (sessionId, lastRunId, lastRunStatus, lastError, sessionParamsJson)
GET  /api/agents/:id/config-revisions?companyId=X → config change history array
GET  /api/companies/:id/agents                   → list all agents in company
```

### Heartbeat Runs
```
GET  /api/heartbeat-runs/:id?companyId=X         → run details (status, error, resultJson, usageJson)
GET  /api/heartbeat-runs/:id/log?offset=0&limitBytes=64000 → run log output
GET  /api/heartbeat-runs/:id/events?afterSeq=0&limit=200 → run events
GET  /api/heartbeat-runs/:id/issues?companyId=X  → issues from this run
```

### Companies
```
GET  /api/companies/:id/dashboard                → dashboard data
GET  /api/companies/:id/secrets                  → secrets list
GET  /api/companies/:id/labels                   → issue labels
GET  /api/companies/:id/skills                   → available skills
GET  /api/companies/:id/budgets/overview         → budget overview
GET  /api/companies/:id/adapters/:type/detect-model → detect available models
POST /api/companies/:id/adapters/:type/test-environment → test adapter connection
```

### Issues
```
GET  /api/companies/:id/issues?status=...&limit=500  → filtered issue list
```

### Adapters
```
GET  /api/companies/:id/adapters/:type/models         → available models
GET  /api/adapters/:type/config-schema                → adapter config schema (may return 404 if not provided)
```

## hermes_local Adapter Configuration

The `hermes_local` adapter connects Paperclip agents to a local Hermes Agent instance.

### Required Fields
- `mode` — Must be non-empty string. Empty → "Adapter failed" on run.
- `model` — Model name string. Empty → no model to execute with.

### Optional Fields
- `effort` — Reasoning effort level (empty = default)
- `variant` — Model variant
- `graceSec` — Grace period in seconds (default: 15)
- `timeoutSec` — Execution timeout in seconds (0 = no timeout)
- `instructionsFilePath` — Path to AGENTS.md with agent instructions
- `instructionsRootPath` — Root path for instructions directory
- `modelReasoningEffort` — Model-specific reasoning effort override

### Agent Error States

| Status | Meaning | Common Fix |
|---|---|---|
| `active` | Agent is ready | N/A |
| `error` | Agent failed last run | Check `lastError` and `resultJson.result`, fix config |
| `paused` | Agent manually paused | Resume from UI |

### Last Run Detail Fields (from runtime-state)
- `lastRunId` — UUID of the last heartbeat run
- `lastRunStatus` — `"failed"`, `"completed"`, etc.
- `lastError` — Error message if any
- `sessionId` — Active session ID (null if no session)
- `sessionParamsJson` — Session parameters including `cwd`, `sessionId`, `promptBundleKey`
- `totalInputTokens` / `totalOutputTokens` — Cumulative token usage
- `totalCostCents` — Cumulative cost in cents

### Detect Model Endpoint

```
GET /api/companies/:id/adapters/hermes_local/detect-model
```

Returns `null` when Hermes Agent is not reachable or configured. Returns model list when available.

## CEO Agent Discovery (Somos Flux Example)

Found during 2026-05-09 session:

- **Agent ID:** 763e73f1-326c-4ba1-8c72-2b860a26e4c1
- **Company ID:** 4dec222b-9a6a-42e5-b477-ac034ff81bd4
- **Role:** `ceo` — orchestrates sub-directors
- **Directors configured:** dir-ghl, dir-traf, dir-int, dir-cont, dir-com, dir-rel
- **Adapter:** hermes_local
- **Instructions:** `/paperclip/instances/default/companies/.../agents/.../instructions/AGENTS.md`

The CEO is an orchestrator agent that routes work to specialized director agents. It has rules against doing executor work itself.
