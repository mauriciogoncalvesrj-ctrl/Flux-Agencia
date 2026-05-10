# Cross-Service Model Audit

How to inventory all AI model references across Hermes Agent, Paperclip agents, and OpenClaw — then reconcile against available models.

## Why

Paperclip `hermes_local` agents inherit their model from Hermes config or explicit `adapterConfig.model`. OpenClaw has its own model list. A mismatch means agents silently fail or use wrong models. When the user reports "some agents use models we don't have", do this audit.

## Step 1: Hermes Agent Model

```bash
grep -A5 "^model:" /opt/data/config.yaml
# Example output:
#   model:
#     default: deepseek-v4-pro
#     provider: opencode-go
#
# Also check auxiliary models:
grep -B1 "model:" /opt/data/config.yaml | grep -v "^--$"
```

## Step 2: Paperclip Agent Models

```bash
# 1. Login to Paperclip API (cookies, not Bearer)
curl -sk -c /tmp/pclip_cookies.txt -X POST \
  "https://paperclip.somosflux.com.br/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -d '{"email":"...","password":"..."}'

# 2. List all agents with adapterConfig
curl -sk -b /tmp/pclip_cookies.txt -H "Accept: application/json" \
  "https://paperclip.somosflux.com.br/api/companies/<companyId>/agents" \
  | python3 -c "
import sys,json
for a in json.load(sys.stdin):
    ac = a.get('adapterConfig',{})
    print(f\"{a['name']:<25} adapter={a['adapterType']:<15} model={ac.get('model','(vazio)')} mode={ac.get('mode','(vazio)')}\")
"
```

**Key insight:** Agents with `adapterType: process` and empty `adapterConfig` are unconfigured — they don't use any model but also can't do LLM work.

## Step 3: OpenClaw Model List

```bash
docker exec openclaw-4vbk-openclaw-1 cat /data/.openclaw/openclaw.json \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)
defaults = d.get('agents',{}).get('defaults',{})
print('Primary:', defaults.get('model',{}).get('primary'))
print('Fallbacks:', defaults.get('model',{}).get('fallbacks'))
models = defaults.get('models',{})
print(f'\nAll configured models ({len(models)}):')
for mid, info in sorted(models.items()):
    print(f'  {mid:<40} {info.get(\"alias\",\"?\")}')
"
```

**Pitfall:** OpenClaw models prefixed `ollama/` route through Nous Research Ollama Cloud API — not local Ollama. Models prefixed `opencode-go/` route through Opencode Go.

## Step 4: Reconcile

Build a table:

| Service | Model | Provider | Available? |
|---|---|---|---|
| Hermes | `deepseek-v4-pro` | opencode-go | ✅ |
| Paperclip CEO | `deepseek-v4-pro` | hermes_local | ✅ |
| OpenClaw | `ollama/gemma4:31b` | ollama cloud | ❌ (not in plan) |

**Removal/replacement rules:**
- Use `docker exec openclaw-... vi /data/.openclaw/openclaw.json` or PATCH the config
- For Paperclip agents: PATCH `adapterConfig` via API (see `references/agent-config-and-tasking.md`)
- For Hermes: edit `/opt/data/config.yaml`

## Step 5: Available Model Sources

Source of truth for which models the user has access to changes over time — always confirm with the user before making changes. Current known providers:

| Provider | API Base | Key |
|---|---|---|
| Opencode Go | `https://opencode.ai/zen/go/v1` | `OPENCODE_GO_API_KEY` |
| Ollama Cloud (Nous) | `https://api.nousresearch.com/v1` | Nous API key |
| OpenAI | `https://api.openai.com/v1` | `OPENAI_API_KEY` |
