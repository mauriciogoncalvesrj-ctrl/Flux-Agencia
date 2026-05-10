# Paperclip Agent Configuration & Tasking Patterns

## Updating Agent Configuration via API

**Important:** Mutation endpoints require a `Origin` header matching a trusted origin, even if Better Auth's origin check is bypassed. The "Board mutation requires trusted browser origin" error means the Origin header is missing or wrong.

### Pitfall: `env` secrets use nested format, NOT flat key-value

The `env` field inside `adapterConfig` expects each secret as a nested object with `type` and `value` fields:

```json
"env": {
  "OPENCODE_GO_API_KEY": {
    "type": "plain",
    "value": "sk-YTWjb..."
  }
}
```

Do **NOT** use flat key-value format — it will be rejected:
```json
// WRONG — will be rejected
"env": {
  "OPENCODE_GO_API_KEY": "sk-YTWjb..."
}
```

### Pattern: PATCH agent adapterType + adapterConfig together

When converting an agent from one adapter type to another (e.g., `process` → `hermes_local`), you must include **both** `adapterType` and `adapterConfig` in the same PATCH body. The PATCH body requires ALL fields you want to set:

```bash
curl -s -b "$COOKIE_JAR" -X PATCH \
  "http://localhost:3100/api/agents/$AGENT_ID?companyId=$COMPANY_ID" \
  -H "Content-Type: application/json" \
  -H "Origin: https://paperclip.somosflux.com.br" \
  -d '{
    "adapterType": "hermes_local",
    "adapterConfig": {
      "mode": "auto",
      "model": "deepseek-v4-pro",
      "effort": "",
      "variant": "",
      "graceSec": 15,
      "timeoutSec": 300,
      "instructionsFilePath": "/paperclip/instances/default/companies/<companyId>/agents/<agentId>/instructions/AGENTS.md",
      "env": {
        "OPENCODE_GO_API_KEY": {
          "type": "plain",
          "value": "sk-..."
        }
      }
    }
  }'
```

**Pitfall:** The old `adapterType` (`process`) has no model — if you only PATCH `adapterConfig` without `adapterType`, the agent still uses the old adapter and the model field is irrelevant.

### Setting API Keys in adapterConfig (nested format)

The `env` field inside `adapterConfig` is passed as environment variables to the spawned Hermes process. Each key is an object with `type` and `value`:

```json
{
  "adapterConfig": {
    "model": "deepseek-v4-pro",
    "mode": "auto",
    "timeoutSec": 300,
    "env": {
      "OPENCODE_GO_API_KEY": {
        "type": "plain",
        "value": "sk-..."
      },
      "OPENROUTER_API_KEY": {
        "type": "plain",
        "value": "sk-or-..."
      }
    }
  }
}
```

**Pitfall:** Flat key-value format (`"KEY": "value"`) is rejected. Always use the nested `{"type": "plain", "value": "..."}` structure.

**Note:** The adapter's `checkApiKeys` function checks `config.env` first (adapter-configured secrets), then falls back to `process.env` (server/host environment).

### Enabling Heartbeat

Agent heartbeat is controlled via `runtimeConfig.heartbeat`:

```bash
curl -s -b "$COOKIE_JAR" -X PATCH \
  "http://localhost:3100/api/agents/<agentId>?companyId=<companyId>" \
  -H "Content-Type: application/json" -H "Origin: http://localhost:3100" \
  -d '{
    "runtimeConfig": {
      "heartbeat": {
        "enabled": true,
        "cooldownSec": 10,
        "intervalSec": 300,
        "wakeOnDemand": true,
        "maxConcurrentRuns": 5
      }
    }
  }'
```

- `intervalSec`: how often the heartbeat ticks (default 300 = 5 min)
- `cooldownSec`: minimum gap between runs (default 10)
- `wakeOnDemand`: allow manual wake-up triggers
- Heartbeat runs show as `invocationSource: "timer"` in heartbeat-runs

### Creating Issues for Agents

Create an issue and assign it to an agent so it's picked up on the next heartbeat:

```bash
curl -s -b "$COOKIE_JAR" -X POST \
  "http://localhost:3100/api/companies/<companyId>/issues" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{
    "title": "Task title",
    "body": "Detailed task description with instructions",
    "priority": "high",
    "assigneeAgentId": "<agentId>",
    "status": "todo"
  }'
```

The response includes the issue `identifier` (e.g., `FLU-5`).

**How agents pick up issues:** On each heartbeat, the agent checks for issues assigned to it:
```
GET /companies/{companyId}/issues?assigneeAgentId={agentId}
```
If issues are found, it works on the highest priority one, then marks it `done` and posts a completion comment.

### Updating Agent Status via API

When an update succeeds, the agent's `status` field transitions:
- `error` → `running` (when a heartbeat run starts successfully)
- `running` → `error` (if a run fails)
- The `lastHeartbeatAt` timestamp is updated on each heartbeat tick

## hermes_local Adapter Execution Flow

1. Heartbeat timer fires → creates a `heartbeat_run` with `invocationSource: "timer"`
2. Paperclip calls the adapter's `execute(ctx)` function
3. Adapter builds a prompt using the template (see `execute.js` in `hermes-paperclip-adapter`)
4. Spawns: `hermes chat -q "<prompt>" -Q -m <model> [--provider <provider>] --yolo --source tool`
5. If `persistSession` is true and a previous session exists, adds `--resume <sessionId>`
6. Waits for the child process, parses output, returns results

## Common Agent API Errors

| Error | Cause | Fix |
|---|---|---|
| `Board mutation requires trusted browser origin` | Missing `Origin` header on PATCH/POST | Add `-H "Origin: http://localhost:3100"` |
| `API route not found` on `/api/agents/:id/wake-up` | Wrong wake-up endpoint | Use heartbeat scheduling instead of manual wake-up |
| `detect-model` returns `null` | Hermes CLI not installed or ~/.hermes/config.yaml missing | Follow hermes-local-adapter-setup.md |
| 401 on `/api/companies/.../issues?assigneeAgentId=...` | Agent using wrong URL prefix (`/api/` before `/companies/`) | This is a known prompt template issue — agent should use `http://127.0.0.1:3100/companies/...` not `http://127.0.0.1:3100/api/companies/...` |
