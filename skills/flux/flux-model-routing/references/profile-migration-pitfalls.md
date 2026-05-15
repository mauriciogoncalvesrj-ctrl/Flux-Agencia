# Profile Migration Pitfalls

> Lições aprendidas durante a migração de Ollama Cloud → GPT/OpenAI Codex + OpenCode Go (2026-05-15)

## 1. Provider não definido em `providers:`

**Problema:** Um profile declara `provider: openai-codex` no `model.provider` mas **não define** `providers.openai-codex` no mesmo config.yaml.

**Sintoma:** O Hermes tenta fazer a chamada mas falha silenciosamente ou retorna erro de provider desconhecido.

**Exemplo (antes — BUG):**
```yaml
# flux-devops/config.yaml
model:
  default: gpt-5.5
  provider: openai-codex    # ← declarado aqui

# ❌ FALTA: providers.openai-codex não está definido!
# O Hermes não sabe como autenticar/conectar ao openai-codex
```

**Exemplo (depois — CORRETO):**
```yaml
# flux-devops/config.yaml
model:
  default: gpt-5.5
  provider: openai-codex

providers:
  opencode-go:
    api_key: ${OPENCODE_GO_API_KEY}
    base_url: https://opencode.ai/zen/go/v1
  openai-codex:              # ← ESSENCIAL: definir o provider
    api_key: ${OPENAI_API_KEY}

fallback_providers:
  - provider: opencode-go
    model: deepseek-v4-pro
  - provider: opencode-go
    model: deepseek-v4-flash
  - provider: opencode-go
    model: kimi-k2.6
```

### Checklist 4 Passos para Configurar Provider

1. ✅ Declarar `model.provider` com o nome do provider
2. ✅ Definir `providers.<nome>` com `api_key` e `base_url` (se necessário)
3. ✅ Configurar `fallback_providers` com modelos alternativos
4. ✅ Testar com uma chamada simples (ex: `hermes run "diga olá" --profile flux-devops`)

---

## 2. `kimi-k2.6` como fallback quebra multi-turn

**Problema:** `kimi-k2.6` via `opencode-go` retorna o campo `reasoning_details` na resposta. Quando esse campo é re-passado como input na chamada seguinte (multi-turn via `delegate_task`), o provider `opencode-go` rejeita com `HTTP 400: "Extra inputs are not permitted, field: messages[N].reasoning_details"`.

**Mitigação:** Manter `kimi-k2.6` apenas como fallback **emergencial de single-turn**. Não usar como primário em nenhum perfil.

**Perfis afetados originalmente:** `flux-orchestrator` (migrado para `deepseek-v4-pro` no commit `599d4da`).

**Referência:** `flux-orchestrator/references/kimi-k2.6-bug-workaround.md`

---

## 3. Visão migrada mas não testada

**Problema:** `flux-vision` foi migrado de `qwen3-vl:235b` (Ollama Cloud) para `qwen3.5-plus` (OpenCode Go), e `auxiliary.vision` no config principal mudou de `provider: custom` (Ollama) para `provider: opencode-go`. Porém **nenhum teste end-to-end foi realizado** para confirmar que `qwen3.5-plus` aceita imagens via `vision_analyze` no Hermes.

**Risco:** Se `qwen3.5-plus` não suportar image input via OpenCode Go, toda a pipeline de visão (OCR, análise de screenshots, QA visual) quebra silenciosamente.

**Ação necessária:** Testar com:
```
vision_analyze(image_url="https://hermes-agent.nousresearch.com/img/logo.png", question="O que tem nesta imagem?")
```

**Fallback planejado:** `qwen3.6-plus` → `gpt-5.5` (se gpt-5.5 tiver visão via openai-codex).

---

## 4. Perfil `flux-compress` — modelo trocado

**Problema:** O `flux-compress` usava `ministral-3:8b` (Ollama Cloud) que não existe no OpenCode Go. Foi migrado para `deepseek-v4-flash`.

**Lições:**
- Nem todo modelo Ollama Cloud tem equivalente no OpenCode Go
- `ministral-3:8b`, `gemma4:31b`, `qwen3-coder-next` são modelos **exclusivos Ollama Cloud**
- Sempre verificar disponibilidade do modelo no provider destino antes de migrar

---

## 5. Main config fallback chain incompleta

**Problema inicial:** A cadeia de fallbacks no `config.yaml` principal ainda referia `glm-5.1` (opencode-go) como primeiro fallback, mas `glm-5.1` não estava mais nos profiles.

**Correção aplicada:** Fallback chain atual:
```
gpt-5.5 → gpt-5.4 → deepseek-v4-flash → deepseek-v4-pro → qwen3.5-plus → kimi-k2.6
```

**Regra:** Manter a fallback chain do main config sincronizada com os profiles. Se um perfil usa `kimi-k2.6` como fallback, o main config também precisa tê-lo como fallback final.

---

## 6. Skills Flux versionadas vs profiles reais

**Problema:** O diretório `/opt/data/skills/flux/` contém a documentação (SKILL.md), mas os profiles reais estão em `/opt/data/profiles/`. As skills **não sincronizam automaticamente** com o GitHub (não são um repositório git).

**Consequência:** Editar a SKILL.md de `flux-model-routing` não altera os profiles reais. Ambos precisam ser mantidos em sincronia manualmente, e as skills precisam ser commitadas no repo `Flux-Agencia` via git.

**Workaround vigente:** Editar SKILL.md → git add/commit/push no symlink reverso.
