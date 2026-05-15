---
name: flux-profile-migration-pitfalls
description: "Catálogo de problemas encontrados durante a migração dos perfis Hermes de Ollama Cloud para GPT + OpenCode Go (2026-05-15). Inclui: provider-not-defined bug, kimi-k2.6 reasoning_details, visão não testada, e checklist de pós-migração. Projetado para ser fundido em flux-model-routing quando skill_manage permitir patch em skills flux/."
version: 1.0.0
metadata:
  hermes:
    tags: [flux-agency, migration, pitfalls, profiles, opencode-go]
    related_skills:
      - flux-model-routing
      - flux-config-audit
---

# Flux Profile Migration Pitfalls

> Registro de problemas encontrados durante a migração dos perfis Hermes de Ollama Cloud para GPT + OpenCode Go (2026-05-15).

## Quando usar

- Após qualquer migração de provider/modelo nos perfis Hermes
- Quando adicionar um novo perfil e ele falhar silenciosamente
- Para validar que a config reflete a documentação (e vice-versa)

---

## Pitfall 1: Provider Declarado mas Não Definido

**Problema:** Um profile referencia um provider em `fallback_providers` ou `model.provider` mas não o define na seção `providers:`. O Hermes falha com `provider "X" not defined`.

**❌ Antes (quebra):**
```yaml
model:
  default: gpt-5.5
  provider: openai-codex   # ← declarado
fallback_providers:
- provider: opencode-go
  model: deepseek-v4-pro
# providers: {}  ← vazio ou ausente!
```

**✅ Depois (corrigido):**
```yaml
model:
  default: gpt-5.5
  provider: openai-codex
providers:
  opencode-go:
    api_key: ${OPENCODE_GO_API_KEY}
    base_url: https://opencode.ai/zen/go/v1
  openai-codex:
    api_key: ${OPENAI_API_KEY}    # ← ESSENCIAL
```

**Aconteceu em:** `flux-devops` (2026-05-15)

---

## Pitfall 2: kimi-k2.6 — reasoning_details Quebra Multi-Turn

**Sintoma:** `HTTP 400: Extra inputs are not permitted, field: messages[N].reasoning_details`

**Causa:** `kimi-k2.6` via `opencode-go` retorna campo `reasoning_details` no response. Quando esse campo é repassado como input na chamada seguinte, o provider rejeita.

**Impacto:** Profiles com `kimi-k2.6` como modelo primário quebram em qualquer conversa multi-turn ou delegate_task.

**Mitigação:** `kimi-k2.6` é fallback-only (último na cadeia). Usar `deepseek-v4-pro` ou `deepseek-v4-flash` para tarefas multi-turn.

**Aconteceu em:** `flux-orchestrator` (2026-05-15, commit 599d4da)

---

## Pitfall 3: Visão Nunca Testada na Prática

**Problema:** A configuração de visão foi migrada de `qwen3-vl:235b`/Ollama para `qwen3.5-plus`/OpenCode Go, mas **nunca foi validada com uma imagem real**.

**Risco:** O card do modelo diz "multimodal" mas no Hermes + OpenCode Go pode:
- Não aceitar `vision_analyze`
- Falhar com imagem via Telegram
- Ter comportamento diferente do esperado

**Checklist de validação:**
- [ ] Enviar uma imagem no Telegram e ver se o modelo a processa
- [ ] Rodar `vision_analyze` diretamente com o perfil `flux-vision`
- [ ] Testar fallback: `qwen3.6-plus` aceita imagem?
- [ ] Se falhar, verificar `auxiliary.vision` no main config

---

## Pitfall 4: Perfil sem Fallback

**Problema:** Profile sem `fallback_providers` fica vulnerável a 429, timeout ou modelo indisponível.

**Mínimo recomendado:**
```yaml
fallback_providers:
- provider: opencode-go
  model: deepseek-v4-flash
```

---

## Checklist de Pós-Migração

- [ ] Todos os perfis refletem o provider correto (sem Ollama Cloud)
- [ ] Cada provider referenciado em `model.provider` e `fallback_providers` está definido em `providers:`
- [ ] Fallback chain completa (mínimo 2 níveis)
- [ ] Visão testada com imagem real (não só pelo card do modelo)
- [ ] SKILL.md do `flux-model-routing` reflete o estado real dos profiles
- [ ] Mudanças commitadas no GitHub

---

## Related Skills

- **flux-model-routing**: Skill principal de roteamento — estes pitfalls devem ser incorporados nela como seção "Common Pitfalls"
- **flux-config-audit**: Metodologia para auditar pendências entre configs e documentação
- **flux-orchestrator**: Usa estes perfis para delegação
