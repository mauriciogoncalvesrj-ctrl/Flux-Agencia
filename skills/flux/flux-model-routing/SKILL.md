---
name: flux-model-routing
description: "Model routing intelligence for Agência Flux after the 2026-05-15 migration away from Ollama Cloud. Maps GPT/OpenAI Codex + OpenCode Go models to operational roles, fallback chains, provider quirks, profile configs, and spending policy. Use before setting model.provider, before delegating tasks to specialist profiles, or when selecting which LLM to use for any Flux pipeline stage."
version: 2.1.0
metadata:
  hermes:
    tags: [flux-agency, llm, routing, opencode-go, openai-codex, deepseek, gpt, models]
    related_skills:
      - flux-orchestrator
      - flux-prompt-engineer
      - multi-agent-architecture
---

# Flux Model Routing — GPT + OpenCode Go

> Política vigente desde **2026-05-15**: cancelar dependência de Ollama Cloud e operar com **GPT/OpenAI Codex + OpenCode Go**.

## Regra central

- Provider operacional padrão: **`opencode-go`**.
- Backbone de volume: **`deepseek-v4-flash`**.
- Backbone de qualidade/análise: **`deepseek-v4-pro`**.
- Camada premium/devops: **`openai-codex` com `gpt-5.5`**.
- Visão primária: **`qwen3.5-plus` via `opencode-go`**.
- Gasto planejado: **80% OpenCode Go / 15% GPT / 5% premium GPT**.
- Não usar Ollama Cloud automaticamente. Referências antigas a `ollama-cloud`, `ollama.com/v1`, `qwen3-vl:235b`, `gemma4:31b`, `ministral-3:8b`, `qwen3-coder-next` e `qwen3.5:cloud` são legado.

## Quick Lookup — Model by Role

| Role | Primary | Provider | Fallback chain |
|---|---|---|---|
| Orchestration / Planner | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `qwen3.5-plus` → `kimi-k2.6` fallback-only |
| DevOps / Code / Debug | `gpt-5.5` | `openai-codex` | `deepseek-v4-pro` → `deepseek-v4-flash` → `kimi-k2.6` fallback-only |
| Research / Web / Docs | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` |
| Creative / Copy / Social | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` |
| Meta Ads / Metrics / Funnel | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` → `gpt-5.5` |
| Vision / OCR / Layout | `qwen3.5-plus` | `opencode-go` | `qwen3.6-plus` → `gpt-5.5` |
| Compression / Triage / Title | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` |

---

## Recommended 7-Profile Architecture

| Perfil | Modelo primário | Provider | Fallbacks | Função |
|---|---|---|---|---|
| `flux-orchestrator` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `qwen3.5-plus` → `kimi-k2.6` | Planejamento, decomposição, coordenação, síntese |
| `flux-devops` | `gpt-5.5` | `openai-codex` | `deepseek-v4-pro` → `deepseek-v4-flash` → `kimi-k2.6` | Código, Hermes, infra, debugging |
| `flux-research` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Pesquisa, benchmarks, documentação |
| `flux-creative` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Copy, ideação, narrativa, engenharia de prompt |
| `flux-meta-ads` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` → `gpt-5.5` | Métricas, funil, diagnóstico de campanhas |
| `flux-vision` | `qwen3.5-plus` | `opencode-go` | `qwen3.6-plus` → `gpt-5.5` | OCR, screenshots, QA visual, análise de referências |
| `flux-compress` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` | Compressão, triagem, títulos, resumos rápidos |

**IMPORTANTE:** `flux-luana` continua não sendo perfil separado; herda `flux-meta-ads` ou `flux-creative` conforme o domínio da tarefa.

## Hermes Mechanism — Profiles vs delegation.*

### Why NOT `delegation.model`?

Setting `delegation.model`, `delegation.provider`, or `delegation.base_url` in config.yaml forces **ALL** sub-agents within a `delegate_task` batch to share one model. This destroys specialization.

### Solution: Hermes Profiles

Each profile is a fully isolated Hermes instance:

- `/opt/data/profiles/{name}/config.yaml`
- `/opt/data/Flux-Agencia/skills/flux/profiles/{name}/config.yaml` mirrors the versioned profile config
- `model.default` + `model.provider` define the LLM for that function
- `delegation.*` remains **empty** so sub-agents inherit the profile model
- Gateway can run multiple profiles in parallel

## Provider quirks

### OpenCode Go (`opencode-go`)

- Endpoint: `https://opencode.ai/zen/go/v1`
- Auth: `OPENCODE_GO_API_KEY` via environment; never commit token values.
- Raw HTTP via Python `urllib`/`requests` may be blocked by Cloudflare (`403`, error code `1010`). Use `curl` with `User-Agent: Hermes-Agent/1.0` for smoke tests.
- Validated model roles:
  - `deepseek-v4-pro`: quality, analysis, orchestration, creative reasoning.
  - `deepseek-v4-flash`: high-volume, fast reporting, triage, compression.
  - `qwen3.5-plus`: primary vision model; high monthly allowance.
  - `qwen3.6-plus`: vision fallback.
- `minimax-m2.5` is **not** vision-capable via OpenCode Go (`HTTP 400`). Do not use it for image analysis.
- `kimi-k2.6` and `mimo-v2.5` are **fallback-only** because both can trigger the `reasoning_details` / `content:null` multi-turn failure pattern.

### OpenAI Codex (`openai-codex`)

- Primary use: `flux-devops`, high-stakes code/config work, difficult debugging, and final premium review.
- Default premium model: `gpt-5.5`.
- Keep usage intentional to preserve the 80/15/5 spending policy.

## Fallback strategy

When primary model fails (429, timeout, model unavailable):

1. Try the configured profile fallback chain.
2. Prefer DeepSeek Flash for speed/volume and DeepSeek Pro for quality/analysis.
3. Escalate to GPT only when the task is high-impact, code-heavy, or requires stronger reliability.
4. Keep `kimi-k2.6` and `mimo-v2.5` as emergency single-turn fallbacks only.
5. Never silently degrade in user-facing summaries — report model/provider switch.

## Common Pitfalls

### 1. Provider declarado mas não definido em `providers:`

**Problema:** Um perfil declara `provider: openai-codex` no `model.provider` mas **não define** `providers.openai-codex` no mesmo config.yaml.

**Sintoma:** Hermes tenta chamar o provider mas falha — provider desconhecido ou sem credenciais.

**Antes (BUG):**
```yaml
model:
  default: gpt-5.5
  provider: openai-codex    # ← declarado mas...
# ❌ FALTA: providers.openai-codex {...}
```

**Depois (CORRETO):**
```yaml
model:
  default: gpt-5.5
  provider: openai-codex
providers:
  openai-codex:              # ← ESSENCIAL
    api_key: ${OPENAI_API_KEY}
  opencode-go:
    api_key: ${OPENCODE_GO_API_KEY}
    base_url: https://opencode.ai/zen/go/v1
```

**Checklist ao configurar qualquer profile:**
1. ✅ `model.provider` declarado
2. ✅ `providers.<nome-do-provider>` definido com `api_key` (e `base_url` se necessário)
3. ✅ `fallback_providers` configurado
4. ✅ Teste rápido: `hermes run "teste" --profile <nome>`

### 2. `kimi-k2.6` quebra multi-turn (delegate_task)

**Problema:** `kimi-k2.6` retorna `reasoning_details` na resposta. Em multi-turn (via `delegate_task`), esse campo é reenviado como input e o provider rejeita com `HTTP 400`.

**Mitigação:** `kimi-k2.6` é **fallback-only** — nunca usar como primário em nenhum perfil. Ver `references/profile-migration-pitfalls.md` e `flux-orchestrator/references/kimi-k2.6-bug-workaround.md`.

### 3. Visão migrada, mas NÃO testada na prática

`flux-vision` foi migrado de `qwen3-vl:235b` (Ollama Cloud) para `qwen3.5-plus` (OpenCode Go). A configuração está no lugar, mas **nenhum teste end-to-end foi feito** para confirmar que `qwen3.5-plus` aceita image input no `vision_analyze` via OpenCode Go.

**Ação necessária:** Testar com uma imagem real antes de confiar na pipeline de visão.

### 4. Perfil `flux-compress` — modelo não existe no novo provider

`ministral-3:8b` e `gemma4:31b` são exclusivos Ollama Cloud. Na migração, `flux-compress` teve que trocar para `deepseek-v4-flash`. Sempre verificar disponibilidade do modelo no provider destino.

### 5. Fallback chain do main config dessincronizada

Após migração, a fallback chain do `config.yaml` principal ainda referia `glm-5.1` (opencode-go). A chain correta é:
```
gpt-5.5 → gpt-5.4 → deepseek-v4-flash → deepseek-v4-pro → qwen3.5-plus → kimi-k2.6
```
Manter sincronizada com os profiles.

**Referência completa:** `references/profile-migration-pitfalls.md`

## References

- `flux-orchestrator/references/model-routing-policy.md` — operational policy
- `flux-orchestrator/references/kimi-k2.6-bug-workaround.md` — reasoning_details bug and fallback-only models
- `flux-prompt-engineer/references/opencode-go-models.md` — model catalog for prompt/creative workflows
- `profiles-legacy` (9 perfis) — arquivos obsoletos da era Ollama Cloud
- `references/profile-migration-pitfalls.md` — 6 pitfalls documentados da migração Ollama → GPT/OpenCode
- Skill: `flux-orchestrator` — decomposition + dispatch protocol
